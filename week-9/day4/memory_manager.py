"""
Memory Manager — Unified Orchestrator
---------------------------------------
Ties together SessionMemory, FAISSVectorStore, and LongTermMemory
into a single interface used by the agent.

Flow implemented here
---------------------
New Query
  → search vector store  (semantic recall)
  → fetch similar context
  → inject into session prompt
  → generate response via Mistral / AutoGen
  → extract + store new facts
  → persist episode to SQLite on session end
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

from memory.session_memory import SessionMemory
from memory.vector_store   import FAISSVectorStore
from memory.long_term      import LongTermMemory


class MemoryManager:
    """
    High-level memory orchestrator used by the AutoGen agent.

    Parameters
    ----------
    session_id : str
        Unique ID for the current user session.
    persist_dir : str | Path
        Directory for FAISS index and SQLite database.
    max_session_turns : int
        Sliding window size for session memory.
    recall_k : int
        Number of similar memories to inject on each turn.
    system_prompt : str | None
        Base system prompt for the agent.
    """

    def __init__(
        self,
        session_id: str = "default",
        persist_dir: str | Path = "memory",
        max_session_turns: int = 20,
        recall_k: int = 4,
        system_prompt: str | None = None,
    ) -> None:
        self.session_id = session_id
        self.recall_k   = recall_k

        persist_dir = Path(persist_dir)

        # ── Three memory layers ──────────────────
        self.session = SessionMemory(
            max_turns=max_session_turns,
            system_prompt=system_prompt or (
                "You are a helpful AI assistant with memory. "
                "Use the context provided to give personalised, accurate answers."
            ),
        )
        self.vector  = FAISSVectorStore(persist_dir=persist_dir)
        self.ltm     = LongTermMemory(db_path=persist_dir / "long_term.db")

    # ── Core query pipeline ──────────────────────

    def prepare_messages(self, user_query: str) -> list[dict]:
        """
        Full memory pipeline for a single user turn.

        1. Search vector store with the query
        2. Build context block from hits
        3. Inject context into session (system prompt)
        4. Append user turn
        5. Return AutoGen-compatible message list
        """
        # Step 1 & 2 — Recall similar memories
        context_block = self.vector.get_context_block(
            query=user_query,
            k=self.recall_k,
            header="[Recalled memories — use these to personalise your response]",
        )

        # Step 3 & 4 — Build message list with context injected
        self.session.add("user", user_query)
        messages = self.session.to_autogen_messages(
            inject_context=context_block if context_block else None
        )

        return messages

    def record_response(self, assistant_reply: str) -> None:
        """
        Store the assistant's reply in session memory.
        Call this after receiving the model's response.
        """
        self.session.add("assistant", assistant_reply)

    def learn_fact(
        self,
        fact: str,
        topic: str = "general",
        confidence: float = 1.0,
    ) -> None:
        """
        Persist a semantic fact to BOTH the vector store and SQLite.

        The vector store enables similarity search; SQLite enables
        exact keyword search and structured queries.
        """
        # Long-term (SQLite) — structured
        self.ltm.upsert_fact(fact, topic=topic, confidence=confidence)
        # Vector (FAISS) — semantic
        self.vector.add(fact, source="fact", topic=topic)
        print(f"[MemoryManager] Learned fact: '{fact[:60]}…'" if len(fact) > 60 else f"[MemoryManager] Learned fact: '{fact}'")

    def save_session(self, summary: str | None = None) -> str:
        """
        At session end:
          1. Save the full transcript to episodic memory (SQLite).
          2. Save the summary to the vector store for future semantic recall.

        Returns the new episode ID.
        """
        transcript = self.session.summary_text()

        # Build auto-summary if none provided
        if not summary:
            lines = [t.content for t in self.session.get_history() if t.role == "user"]
            summary = "Session topics: " + "; ".join(lines[:5])

        episode_id = self.ltm.save_episode(
            content=transcript,
            session_id=self.session_id,
            summary=summary,
        )
        # Index the summary in FAISS so it can be recalled in future sessions
        self.vector.add(
            summary,
            source="episodic",
            session_id=self.session_id,
            episode_id=episode_id,
        )
        print(f"[MemoryManager] Session saved as episode {episode_id[:8]}…")
        return episode_id

    def extract_and_learn_facts(self, text: str, topic: str = "general") -> list[str]:
        """
        Heuristic fact extractor: splits text on sentence boundaries and
        stores sentences that look like facts (contain "is", "are", "was", etc.).

        In production, replace this with an LLM-based extractor call.
        """
        fact_patterns = re.compile(
            r"\b(is|are|was|were|has|have|can|will|should|must|loves?|prefers?|uses?|works?)\b",
            re.IGNORECASE,
        )
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        stored: list[str] = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and fact_patterns.search(sentence):
                self.learn_fact(sentence, topic=topic)
                stored.append(sentence)

        return stored

    # ── Diagnostics ──────────────────────────────

    def memory_summary(self) -> dict:
        return {
            "session_turns":  len(self.session),
            "vector_chunks":  self.vector.size,
            "db_stats":       self.ltm.stats(),
        }

    def __repr__(self) -> str:
        s = self.memory_summary()
        return (
            f"MemoryManager("
            f"session={s['session_turns']} turns, "
            f"vector={s['vector_chunks']} chunks, "
            f"episodes={s['db_stats']['episodes']}, "
            f"facts={s['db_stats']['facts']})"
        )