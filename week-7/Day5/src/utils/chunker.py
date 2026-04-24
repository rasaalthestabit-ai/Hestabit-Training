from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text):
    words = text.split()
    chunks = []

    step = CHUNK_SIZE - CHUNK_OVERLAP

    for i in range(0, len(words), step):
        chunk_words = words[i:i + CHUNK_SIZE]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

    return chunks


def chunk_documents(documents):
    all_chunks = []

    for doc in documents:
        text_chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(text_chunks):
            chunk_doc = {
                "text": chunk,
                "metadata": {
                    **doc.get("metadata", {}),
                    "chunk_id": i
                }
            }

            all_chunks.append(chunk_doc)

    return all_chunks