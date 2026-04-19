import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import sqlite3
import os

DB_PATH = "memory/long_term.db"
VECTOR_DIM = 384

class VectorStore:
    def __init__(self):
        print("Loading sentence transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(VECTOR_DIM)
        self.texts = []
        print("Vector store initialized!")

    def add_text(self, text):
        """Convert text to embedding and store in FAISS"""
        embedding = self.model.encode([text])
        embedding = np.array(embedding, dtype=np.float32)
        self.index.add(embedding)
        self.texts.append(text)
        print(f"Stored in FAISS: {text[:50]}...")

    def search(self, query, top_k=3):
        """Search for similar context in FAISS"""
        if self.index.ntotal == 0:
            print("Vector store is empty!")
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding, dtype=np.float32)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "distance": distances[0][i]
                })

        return results

    def load_from_db(self, user_id):
        """Load only this user's facts from long_term.db into FAISS"""
        if not os.path.exists(DB_PATH):
            print("No long-term memory database found!")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT fact FROM long_term_memory WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"No memory found for user: {user_id}")
            return

        for row in rows:
            self.add_text(row[0])

        print(f"Loaded {len(rows)} facts for user: {user_id}")

    def get_context_for_query(self, query):
        """Get relevant context for a query"""
        results = self.search(query)

        if not results:
            return ""

        context = "Relevant memory context:\n"
        for r in results:
            context += f"- {r['text']}\n"

        return context