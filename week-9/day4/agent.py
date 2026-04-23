"""
Agent — Groq with Full Memory System
--------------------------------------
Cross-session memory fixes:
  1. Auto-saves session on quit / Ctrl+C (no need to type 'save')
  2. On startup, syncs all SQLite facts + episodes back into FAISS
     so the agent recalls you even after a full process restart
  3. Direct Groq SDK — clean multi-turn context every turn

Run (CLI):     python agent.py
Run (server):  uvicorn agent:app --reload --port 8000

.env:
    GROQ_API_KEY=your_key_here
    GROQ_MODEL=llama-3.3-70b-versatile
    MEMORY_DIR=memory
"""

from __future__ import annotations

import os
import uuid
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from pydantic import BaseModel

from memory_manager import MemoryManager

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
PERSIST_DIR  = os.getenv("MEMORY_DIR", "memory")

groq_client  = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful AI assistant with persistent memory across conversations. "
    "You remember facts about the user, prior conversations, and learned knowledge. "
    "Use any recalled memories in your context to give personalised, accurate answers. "
    "When the user shares personal information or new facts, acknowledge and note them."
)

# ─────────────────────────────────────────────
# SQLite → FAISS bootstrap (cross-session recall)
# ─────────────────────────────────────────────

def _sync_sqlite_to_faiss(mm: MemoryManager) -> None:
    """
    On every startup, reload persisted SQLite facts + episode summaries
    into FAISS so the agent can recall them via similarity search.

    FAISS already loads its .bin file on init — this syncs anything
    saved to SQLite that isn't already in the FAISS index.
    """
    existing_texts = {c.text for c in mm.vector._chunks}
    synced = 0

    # ── Semantic facts ──────────────────────────
    for f in mm.ltm.get_facts(limit=9999):
        if f["fact"] not in existing_texts:
            mm.vector.add(f["fact"], source="fact", topic=f.get("topic", "general"))
            existing_texts.add(f["fact"])
            synced += 1

    # ── Episodic summaries ──────────────────────
    for ep in mm.ltm.recent_episodes(n=9999):
        summary = ep.get("summary") or ""
        if summary and summary not in existing_texts:
            mm.vector.add(
                summary,
                source="episodic",
                session_id=ep.get("session_id", ""),
                episode_id=ep.get("id", ""),
            )
            existing_texts.add(summary)
            synced += 1

    if synced:
        print(f"[Memory] Synced {synced} entries from SQLite → FAISS (cross-session recall ready)")
    else:
        print("[Memory] FAISS already up-to-date with SQLite")

# ─────────────────────────────────────────────
# Session registry
# ─────────────────────────────────────────────

_sessions: dict[str, MemoryManager] = {}


def get_or_create_session(session_id: str) -> MemoryManager:
    if session_id not in _sessions:
        mm = MemoryManager(
            session_id=session_id,
            persist_dir=PERSIST_DIR,
            max_session_turns=20,
            recall_k=4,
            system_prompt=SYSTEM_PROMPT,
        )
        # Bootstrap FAISS with all persisted SQLite data
        _sync_sqlite_to_faiss(mm)
        _sessions[session_id] = mm
    return _sessions[session_id]


# ─────────────────────────────────────────────
# Core agent turn
# ─────────────────────────────────────────────

def run_agent_turn(memory: MemoryManager, user_message: str) -> str:
    """
    Memory-augmented single turn:
      1. Search FAISS → recalled past memories (cross-session)
      2. Inject recalled context into system prompt
      3. Build full conversation history from session memory
      4. Call Groq → get reply
      5. Store both turns in session memory
      6. Extract + persist new facts to FAISS + SQLite immediately
    """

    # Step 1 & 2 — Recall + inject
    context_block = memory.vector.get_context_block(
        query=user_message,
        k=memory.recall_k,
        header="[Recalled memories — use to personalise your response]",
    )
    system_content = SYSTEM_PROMPT
    if context_block:
        system_content += f"\n\n{context_block}"

    # Step 3 — Full message list: system + history + current user message
    messages = [{"role": "system", "content": system_content}]
    for turn in memory.session.get_history():
        messages.append({"role": turn.role, "content": turn.content})
    messages.append({"role": "user", "content": user_message})

    # Step 4 — Call Groq
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    reply_text = response.choices[0].message.content.strip()

    # Step 5 — Save turns to session memory
    memory.session.add("user", user_message)
    memory.session.add("assistant", reply_text)

    # Step 6 — Extract + persist facts immediately (so they survive even without 'save')
    memory.extract_and_learn_facts(user_message, topic="user_statement")

    return reply_text


# ─────────────────────────────────────────────
# CLI — with auto-save on exit
# ─────────────────────────────────────────────

if __name__ == "__main__":
    session_id = "cli_test"
    memory     = get_or_create_session(session_id)

    print("=" * 55)
    print(f"  Day 4 — Memory Agent  |  Model: {GROQ_MODEL}")
    print("=" * 55)
    print("Commands: 'quit' | 'stats' | 'save'\n")

    def _auto_save():
        """Save session silently on any exit path."""
        if memory and len(memory.session) > 0:
            try:
                eid = memory.save_session()
                print(f"\n[Memory] Session auto-saved → episode {eid[:8]}...")
            except Exception:
                pass

    import atexit
    atexit.register(_auto_save)   # ← fires on quit, Ctrl+C, or any crash

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "stats":
            s = memory.memory_summary()
            print(f"\n[Memory Stats]")
            print(f"  Session turns : {s['session_turns']}")
            print(f"  Vector chunks : {s['vector_chunks']}")
            print(f"  Episodes      : {s['db_stats']['episodes']}")
            print(f"  Facts stored  : {s['db_stats']['facts']}")
            continue

        if user_input.lower() == "save":
            eid = memory.save_session()
            print(f"[Session saved → episode: {eid[:8]}...]")
            continue   # don't break — keep chatting after manual save

        try:
            reply = run_agent_turn(memory, user_input)
            print(f"\nAgent: {reply}\n")
        except Exception as e:
            print(f"\n[Error] {e}\n")