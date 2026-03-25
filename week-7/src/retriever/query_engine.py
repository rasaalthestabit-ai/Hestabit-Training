from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore


class QueryEngine:
    def __init__(self):
        self.embedder = Embedder()
        self.store = FAISSStore(dim=384)
        self.store.load()

    def query(self, text, k=5):
        query_vector = self.embedder.embed([text])
        results = self.store.search(query_vector, k)
        return results


# ---------------------------
# INTERACTIVE MODE
# ---------------------------
if __name__ == "__main__":
    engine = QueryEngine()

    print("\n🤖 RAG Query Engine Ready!")

    while True:
        print("Type your question below (type 'exit' to quit)\n")
        user_query = input("💬 Your Question: ")

        # Exit condition
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Exiting... Goodbye!")
            break

        # Run query
        results = engine.query(user_query)

        # Display results
        print("\n📚 Top Results:\n")

        for i, r in enumerate(results, 1):
            print(f"--- Result {i} ---")
            print("📄 Source:", r.get("source"))
            print("🧩 Chunk ID:", r.get("chunk_id"))
            print("📝 Text:", r.get("text"))
            print()

        print("=" * 50)