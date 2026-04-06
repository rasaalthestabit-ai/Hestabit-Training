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
            self.llm
        )

    # -------------------------------
    # TEXT → IMAGE
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
    # IMAGE → IMAGE
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
    # IMAGE → TEXT (FIXED VQA)
    # -------------------------------
    def image_to_text(self, image_path, question, k=3):
        try:
            # ---------------------------
            # STEP 1: Generate caption
            # ---------------------------
            caption = self.generator.generate_caption(image_path)

            # ---------------------------
            # STEP 2: Direct VQA
            # ---------------------------
            direct_answer = self.generator.answer_question(image_path, question)

            # ---------------------------
            # STEP 3: LLM refinement (VERY IMPORTANT)
            # ---------------------------
            prompt = f"""
    You are a vision AI assistant.

    Image description:
    {caption}

    User question:
    {question}

    Initial answer:
    {direct_answer}

    Give a clear, specific, and correct answer.
    Avoid generic words like "infographic" unless absolutely certain.
    """

            final_answer = self.llm.generate(prompt)

            return final_answer

        except Exception as e:
            return f"Error: {str(e)}"