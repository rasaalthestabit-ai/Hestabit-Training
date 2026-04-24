import os
import json
from tqdm import tqdm

from utils.loaders import load_pdf, load_csv, load_docx, load_image
from utils.cleaner import clean_text
from utils.chunker import chunk_text
from utils.metadata import create_metadata

from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore


# ✅ PATHS FOR SAVING
CLEANED_PATH = "src/data/cleaned/"
CHUNKS_PATH = "src/data/chunks/"


# ---------------------------
# FILE TYPE LOADER
# ---------------------------
def get_loader(file):
    if file.endswith(".pdf"):
        return load_pdf
    elif file.endswith(".csv"):
        return load_csv
    elif file.endswith(".docx"):
        return load_docx
    elif file.endswith((".png", ".jpg", ".jpeg")):
        return load_image
    return None


# ---------------------------
# SAVE CLEANED TEXT
# ---------------------------
def save_cleaned_text(file_name, text):
    os.makedirs(CLEANED_PATH, exist_ok=True)

    file_path = os.path.join(CLEANED_PATH, f"{file_name}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------
# SAVE CHUNKS
# ---------------------------
def save_chunks(chunks, metadata_list):
    os.makedirs(CHUNKS_PATH, exist_ok=True)

    for i, (chunk, meta) in enumerate(zip(chunks, metadata_list)):
        file_path = os.path.join(CHUNKS_PATH, f"chunk_{i}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "text": chunk,
                "metadata": meta
            }, f, ensure_ascii=False, indent=2)


# ---------------------------
# MAIN INGESTION PIPELINE
# ---------------------------
def run_ingestion(data_path):
    embedder = Embedder()

    all_chunks = []
    all_metadata = []

    for root, _, files in os.walk(data_path):
        for file in files:
            path = os.path.join(root, file)

            print(f"📄 Processing file: {file}")

            loader = get_loader(file)
            if loader is None:
                continue

            docs = loader(path)

            for doc_id, doc in enumerate(docs):
                cleaned = clean_text(doc["text"])

                # ✅ SAVE CLEANED TEXT
                file_id = f"{file}_{doc_id}"
                save_cleaned_text(file_id, cleaned)

                chunks = chunk_text(cleaned)

                for i, chunk in enumerate(chunks):

                    # ✅ Store chunk text for embeddings
                    all_chunks.append(chunk)

                    # 🔥 Store metadata + TEXT together (CRITICAL)
                    all_metadata.append({
                        **create_metadata(doc, i),
                        "text": chunk
                    })

    print(f"\n✅ Total chunks: {len(all_chunks)}")

    # ✅ SAVE CHUNKS TO DISK
    save_chunks(all_chunks, all_metadata)

    print("🚀 Generating embeddings...")
    vectors = embedder.embed(all_chunks)

    print("✅ Embeddings generated!")
    print("💾 Storing in FAISS...")

    store = FAISSStore(dim=len(vectors[0]))
    store.add(vectors, all_metadata)
    store.save()

    print("🎉 Ingestion Complete!")


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    run_ingestion("src/data/raw")