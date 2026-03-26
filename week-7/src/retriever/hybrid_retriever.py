from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore


class HybridRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = FAISSStore(dim=384)
        self.store.load()

    # ---------------------------
    # SEMANTIC SEARCH (EXISTING)
    # ---------------------------
    def semantic_search(self, query, k=10):
        q_vec = self.embedder.embed([query])
        return self.store.search(q_vec, k)

    # ---------------------------
    # KEYWORD SEARCH (NEW)
    # ---------------------------
    def keyword_search(self, query, k=10):
        results = []

        for doc in self.store.metadata:
            text = doc.get("text", "").lower()

            # simple keyword match score
            score = sum(word in text for word in query.lower().split())

            if score > 0:
                doc["keyword_score"] = score
                results.append(doc)

        # sort by keyword score
        results.sort(key=lambda x: x["keyword_score"], reverse=True)

        return results[:k]

    # ---------------------------
    # HYBRID COMBINE
    # ---------------------------
    def hybrid_search(self, query, k=5):
        semantic_results = self.semantic_search(query, k=10)
        keyword_results = self.keyword_search(query, k=10)

        # merge results
        combined = semantic_results + keyword_results

        return combined[:k]