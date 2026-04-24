from rank_bm25 import BM25Okapi
import numpy as np

from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore


class HybridRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = FAISSStore(dim=384)

        # 🔥 Precompute BM25 ONCE
        self.docs = [doc["text"] for doc in self.store.metadata]
        self.tokenized_docs = [doc.split() for doc in self.docs]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def semantic_search(self, query, k=10):
        q_vec = self.embedder.embed([query])
        return self.store.search(q_vec, k)

    def keyword_search(self, query, k=10):
        scores = self.bm25.get_scores(query.split())

        top_k_idx = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_k_idx:
            doc = self.store.metadata[idx].copy()
            doc["bm25_score"] = float(scores[idx])
            results.append(doc)

        return results

    def hybrid_search(self, query, k=5):
        sem = self.semantic_search(query, k=10)
        key = self.keyword_search(query, k=10)

        combined = {}

        # Merge with scoring
        for doc in sem:
            key_id = doc["text"]
            combined[key_id] = doc
            combined[key_id]["score"] = 0.7

        for doc in key:
            key_id = doc["text"]
            if key_id in combined:
                combined[key_id]["score"] += 0.3
            else:
                combined[key_id] = doc
                combined[key_id]["score"] = 0.3

        return list(combined.values())[:k]