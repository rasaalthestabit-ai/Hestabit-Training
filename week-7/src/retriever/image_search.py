from embeddings.clip_embedder import CLIPEmbedder
from vectorstore.faiss_store import FAISSStore
from generator.image_generator import ImageGenerator
from generator.contextual_caption_generator import ContextualCaptionGenerator
from generator.llm_client import LLMClient


class ImageSearch:
    def __init__(self):
        self.embedder = CLIPEmbedder()
        self.store = FAISSStore(
            dim=512,
            index_path="src/vectorstore/image.index"
        )
        self.generator = ImageGenerator()
        self.llm = LLMClient()
        self.context_generator = ContextualCaptionGenerator(
        self.generator,
        self.llm)

    # -------------------------------
    # TEXT → IMAGE (WITH GENERATED CAPTION)
    # -------------------------------
    def text_to_image(self, query, k=3):
        vector = self.embedder.embed_text(query)
        results = self.store.search(vector, k)

        final_results = []

        for r in results:
            context = self.context_generator.generate(r["path"])

            final_results.append({
                "image": r["path"],
                "final_caption": context["final"]
            })

        return final_results

    # -------------------------------
    # IMAGE → IMAGE (WITH GENERATED CAPTION)
    # -------------------------------
    def image_to_image(self, image_path, k=3):
        vector = self.embedder.embed_image(image_path)
        results = self.store.search(vector, k)

        final_results = []

        for r in results:
            context = self.context_generator.generate(r["path"])

            final_results.append({
                "image": r["path"],
                "final_caption": context["final"]
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