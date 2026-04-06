import os
from fastapi import FastAPI
from pydantic import BaseModel

from memory.memory_store import MemoryStore
from evaluation.rag_eval import RAGEvaluator

from retriever.image_search import ImageSearch
from generator.llm_client import LLMClient
from pipelines.sql_pipeline import SQLPipeline
from retriever.query_engine import QueryEngine

# -----------------------------
# INIT
# -----------------------------
app = FastAPI()

memory = MemoryStore()
llm = LLMClient()
evaluator = RAGEvaluator(llm)
image_search = ImageSearch()

sql_pipeline = SQLPipeline(db_path="src/data/raw/db.sqlite")
query_engine = QueryEngine()


class QueryRequest(BaseModel):
    query: str


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_relevant_memory(query, k=2):
    try:
        memory_context = memory.get_context()
        if not memory_context:
            return ""

        memory_lines = memory_context.split("\n")[-k:]
        memory_context = "\n".join(memory_lines)

        if query.lower() not in memory_context.lower():
            return ""

        return memory_context
    except:
        return ""


def is_context_relevant(context):
    return len(context.strip().split()) > 20


# 🔥 NEW: Safe score conversion (fixes string issue)
def safe_score(score):
    try:
        return float(score)
    except:
        return 0.0


# -----------------------------
# TEXT (RAG + FALLBACK)
# -----------------------------
@app.post("/ask")
def ask_text(req: QueryRequest):
    try:
        user_query = req.query

        # STEP 1: Retrieve from docs
        results, context = query_engine.query(user_query, k=5)

        # STEP 2: Decide source
        if is_context_relevant(context):
            source = "documents"

            # 🔥 UPDATED PROMPT (fallback enabled)
            prompt = f"""
You are a helpful assistant.

First, try to answer using ONLY the provided context.

If the answer is clearly present:
- Answer using the context.

If the answer is NOT present:
- Say: "Not found in provided documents."
- Then provide the best possible answer using your own knowledge.

Context:
{context}

Question:
{user_query}

Answer:
"""
        else:
            source = "general"

            prompt = f"""
You are a helpful assistant.

No relevant documents were found.
Answer using general knowledge.

Question:
{user_query}

Answer:
"""

        answer = llm.generate(prompt)

        # STEP 3: Evaluation
        memory_context = get_relevant_memory(user_query)

        refined = evaluator.refine_answer(memory_context, answer)
        faithful = evaluator.hallucination_check(context, refined)

        # 🔥 FIXED
        score = safe_score(evaluator.faithfulness_score(context, refined))

        memory.add(user_query, refined)

        return {
            "answer": refined,
            "source": source,
            "faithful": faithful,
            "score": score
        }

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# IMAGE (RAG-AWARE)
# -----------------------------
@app.post("/ask-image")
def ask_image(req: QueryRequest):
    try:
        results, context = query_engine.query(req.query, k=3)

        enhanced_query = req.query
        if is_context_relevant(context):
            enhanced_query += " " + context[:200]

        images = image_search.text_to_image(enhanced_query)

        return {
            "results": images
        }

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# SQL (RAG + PIPELINE)
# -----------------------------
@app.post("/ask-sql")
def ask_sql(req: QueryRequest):
    try:
        user_query = req.query

        # STEP 1: RAG context
        results, context = query_engine.query(user_query, k=5)

        if is_context_relevant(context):
            user_query = f"{user_query}\n\nContext:\n{context}"

        # STEP 2: SQL pipeline
        pipeline_result = sql_pipeline.run(user_query)

        sql_query = pipeline_result["sql"]
        result = pipeline_result["result"]
        answer = pipeline_result["answer"]

        # STEP 3: Evaluation
        memory_context = get_relevant_memory(req.query)

        refined = evaluator.refine_answer(memory_context, answer)
        def flatten_result(res):
            flat = []
            for row in res:
                if isinstance(row, (list, tuple)):
                    flat.extend([str(x) for x in row])
                else:
                    flat.append(str(row))
            return flat

        flat_result = flatten_result(result)
        answer_str = refined.lower()

        # 🔥 Deterministic grounding check
        if any(item.lower() in answer_str for item in flat_result):
            faithful = True
            score = 0.95
        else:
            faithful = False
            score = 0.3

        memory.add(req.query, refined)

        return {
            "sql": sql_query,
            "result": result,
            "answer": refined,
            "faithful": faithful,
            "score": score
        }

    except Exception as e:
        return {"error": str(e)}