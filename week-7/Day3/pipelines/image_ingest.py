import os
from PIL import Image

from embeddings.clip_embedder import CLIPEmbedder
from vectorstore.faiss_store import FAISSStore


class FastImageIngestor:
    def __init__(self):
        self.embedder = CLIPEmbedder()

        self.store = FAISSStore(
            dim=512,
            index_path="src/vectorstore/image.index"
        )

    def preprocess(self, path):
        return Image.open(path).convert("RGB").resize((224, 224))

    def ingest(self, folder_path):
        image_paths = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        print(f"🚀 Found {len(image_paths)} images")

        all_vectors = []
        all_metadata = []

        batch_size = 16

        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]

            images = [self.preprocess(p) for p in batch_paths]

            embeddings = self.embedder.batch_embed_images(images)

            for path, emb in zip(batch_paths, embeddings):
                all_vectors.append(emb.reshape(-1))

                all_metadata.append({
                    "type": "image",
                    "path": path,
                    "file": os.path.basename(path)
                })

            print(f"✅ Processed batch {i//batch_size + 1}")

        if all_vectors:
            self.store.add(all_vectors, all_metadata)
            self.store.save()

        print("🎉 FAST ingestion complete!")


if __name__ == "__main__":
    folder_path = "src/data/raw/Images"
    FastImageIngestor().ingest(folder_path)