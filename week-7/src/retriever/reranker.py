import numpy as np


class Reranker:
    def __init__(self, embedder):
        self.embedder = embedder

    def rerank(self, query, docs):
        query_vec = self.embedder.embed([query])[0]

        scored_docs = []

        for doc in docs:
            doc_vec = self.embedder.embed([doc["text"]])[0]

            # cosine similarity
            score = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )

            doc["score"] = float(score)
            scored_docs.append(doc)

        # sort by score
        scored_docs.sort(key=lambda x: x["score"], reverse=True)

        return scored_docs