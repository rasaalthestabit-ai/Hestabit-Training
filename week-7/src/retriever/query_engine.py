from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore

from retriever.hybrid_retriever import HybridRetriever
from retriever.reranker import Reranker
from pipelines.context_builder import ContextBuilder


class QueryEngine:
    def __init__(self):
        # ✅ Keep original components (Day 1 compatibility)
        self.embedder = Embedder()
        self.store = FAISSStore(dim=384)
        self.store.load()

        # ✅ Add new components (Day 2)
        self.retriever = HybridRetriever()
        self.reranker = Reranker(self.embedder)
        self.builder = ContextBuilder()

    def query(self, text, k=5, filters=None):
        # ---------------------------
        # STEP 1: HYBRID RETRIEVAL
        # ---------------------------
        results = self.retriever.hybrid_search(text, k=10)

        # ---------------------------
        # STEP 2: APPLY FILTERS
        # ---------------------------
        if filters:
            results = self.builder.apply_filters(results, filters)

        # ---------------------------
        # STEP 3: RERANK
        # ---------------------------
        results = self.reranker.rerank(text, results)

        # ---------------------------
        # STEP 4: DEDUPLICATE
        # ---------------------------
        results = self.builder.deduplicate(results)

        # ---------------------------
        # STEP 5: TOP-K SELECTION
        # ---------------------------
        top_results = results[:k]

        # ---------------------------
        # STEP 6: BUILD CONTEXT
        # ---------------------------
        context = self.builder.build(top_results)

        return top_results, context


# ---------------------------
# INTERACTIVE MODE
# ---------------------------
if __name__ == "__main__":
    engine = QueryEngine()

    print("\n🤖 Advanced RAG Query Engine Ready!")

    while True:
        print("\nType your question below (type 'exit' to quit)\n")
        user_query = input("💬 Your Question: ")

        # Exit condition
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Exiting... Goodbye!")
            break

        # OPTIONAL: Add filters later if needed
        filters = {}

        # Run query
        results, context = engine.query(user_query, k=5, filters=filters)

        # Display results
        print("\n📚 Top Results:\n")

        for i, r in enumerate(results, 1):
            print(f"--- Result {i} ---")
            print("📄 Source:", r.get("source"))
            print("🧩 Chunk ID:", r.get("chunk_id"))
            print("⭐ Score:", round(r.get("score", 0), 4))
            print("📝 Text:", r.get("text"))
            print()

        print("=" * 50)

        # ✅ NEW: Show final context (important for Day 2)
        print("\n🧠 FINAL CONTEXT (LLM INPUT):\n")
        print(context)

        print("\n" + "=" * 50)