from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed(self, texts):
        return self.model.encode(
            texts,
            batch_size=32,           # ✅ Faster processing
            show_progress_bar=True
        )