from embeddings.clip_embedder import CLIPEmbedder
from vectorstore.faiss_store import FAISSStore
from generator.image_generator import ImageGenerator


class ImageSearch:
    def __init__(self):
        self.embedder = CLIPEmbedder()
        self.store = FAISSStore(
            dim=512,
            index_path="src/vectorstore/image.index"
        )
        self.generator = ImageGenerator()

    # -------------------------------
    # TEXT → IMAGE (WITH GENERATED CAPTION)
    # -------------------------------
    def text_to_image(self, query, k=3):
        vector = self.embedder.embed_text(query)
        results = self.store.search(vector, k)

        if not results:
            return []

        final_results = []

        for r in results:
            caption = self.generator.generate_caption(r["path"])

            final_results.append({
                "image": r["path"],
                "stored_caption": r.get("caption"),
                "generated_caption": caption
            })

        return final_results

    # -------------------------------
    # IMAGE → IMAGE (WITH GENERATED CAPTION)
    # -------------------------------
    def image_to_image(self, image_path, k=3):
        vector = self.embedder.embed_image(image_path)
        results = self.store.search(vector, k)

        if not results:
            return []

        final_results = []

        for r in results:
            caption = self.generator.generate_caption(r["path"])

            final_results.append({
                "image": r["path"],
                "generated_caption": caption
            })

        return final_results

    # -------------------------------
    # IMAGE → TEXT (FULL QA)
    # -------------------------------
    def image_to_text(self, image_path, question, k=3):
        vector = self.embedder.embed_image(image_path)
        results = self.store.search(vector, k)

        if not results:
            return "❌ No context found"

        best = results[0]

        # 🔥 Direct VQA
        answer = self.generator.answer_question(best["path"], question)

        return answer