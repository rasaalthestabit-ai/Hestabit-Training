import os
import pytesseract
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from embeddings.clip_embedder import CLIPEmbedder
from vectorstore.faiss_store import FAISSStore


class ImageIngestor:
    def __init__(self):
        self.embedder = CLIPEmbedder()

        self.store = FAISSStore(
            dim=512,
            index_path="src/vectorstore/image.index"
        )

        # BLIP for captions
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def extract_ocr(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)

    def generate_caption(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt")

        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)

    def ingest(self, folder_path):
        all_vectors = []
        all_metadata = []

        for file in os.listdir(folder_path):
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            path = os.path.join(folder_path, file)
            print(f"Processing {file}...")

            # OCR
            ocr_text = self.extract_ocr(path)

            # Caption
            caption = self.generate_caption(path)

            # Embedding
            embedding = self.embedder.embed_image(path)

            embedding = embedding.reshape(-1)

            all_vectors.append(embedding)

            all_metadata.append({
                "type": "image",
                "path": path,
                "file": file,
                "ocr": ocr_text,
                "caption": caption
            })

        # ✅ Add in batch (correct)
        if all_vectors:
            self.store.add(all_vectors, all_metadata)
            self.store.save()

        print("\n✅ Image ingestion completed!")


if __name__ == "__main__":
    folder_path = "src/data/raw/Images"

    ingestor = ImageIngestor()
    ingestor.ingest(folder_path)