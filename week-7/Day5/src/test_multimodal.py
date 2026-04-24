import os
from embeddings.clip_embedder import CLIPEmbedder
from vectorstore.faiss_store import FAISSStore
from generator.llm_client import LLMClient
from retriever.image_search import ImageSearch
from generator.image_generator import ImageGenerator
from generator.contextual_caption_generator import ContextualCaptionGenerator



class MultimodalTester:
    def __init__(self):
        print("🚀 Initializing Multimodal Tester...")

        self.embedder = CLIPEmbedder()

        self.image_store = FAISSStore(
            dim=512,
            index_path="src/vectorstore/image.index"
        )

        self.llm = LLMClient()

        self.search = ImageSearch()

        self.image_generator = ImageGenerator()

        self.context_generator = ContextualCaptionGenerator(
            self.image_generator,
            self.llm
        )

        print("✅ System ready!\n")

    # -------------------------------
    # 1. TEXT → IMAGE
    # -------------------------------
    def text_to_image(self):
        query = input("\n📝 Enter text query: ")

        results = self.search.text_to_image(query)

        for i, r in enumerate(results):
            print(f"\n{i+1}. 📁 Image: {r['image']}")
            print(f"   🤖 Final Caption: {r['final_caption']}")

    # -------------------------------
    # 2. IMAGE → IMAGE
    # -------------------------------
    def image_to_image(self):
        image_path = input("\n🖼️ Enter image path: ")

        if not os.path.exists(image_path):
            print("❌ Image not found!")
            return

        results = self.search.image_to_image(image_path)

        for i, r in enumerate(results):
            print(f"\n{i+1}. 📁 Image: {r['image']}")
            print(f"   🤖 Final Caption: {r['final_caption']}")

    # -------------------------------
    # 3. IMAGE → TEXT ANSWER
    # -------------------------------
    def image_to_text(self):
        image_path = input("\n🖼️ Enter image path: ")

        if not os.path.exists(image_path):
            print("❌ Image not found!")
            return

        question = input("❓ Ask a question about this image: ")

        # Step 1: Embed image
        query_embedding = self.embedder.embed_image(image_path)

        # Step 2: Retrieve similar images
        results = self.image_store.search(query_embedding, k=3)

        # Step 3: Build context
        context = ""
        for r in results:
            context += r.get("caption", "") + "\n"
            context += r.get("ocr", "") + "\n"

        print("\n📄 Context sent to LLM:")
        print(context if context else "⚠️ No OCR/Caption found")

        # Step 4: LLM response
        prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.generate(prompt)

        print("\n🤖 Answer:")
        print(response)

    # -------------------------------
    # MAIN MENU
    # -------------------------------
    def run(self):
        while True:
            choice = input("""
==============================
🎯 SELECT QUERY MODE
==============================
1. Text → Image
2. Image → Image
3. Image → Text Answer
4. Exit
==============================
Enter choice: """)

            if choice == "1":
                self.text_to_image()
            elif choice == "2":
                self.image_to_image()
            elif choice == "3":
                self.image_to_text()
            elif choice == "4":
                print("👋 Exiting...")
                break
            else:
                print("❌ Invalid choice!")


if __name__ == "__main__":
    tester = MultimodalTester()
    tester.run()