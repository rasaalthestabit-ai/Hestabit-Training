def create_metadata(doc, chunk_id):
    return {
        "source": doc["source"],
        "page": doc["page"],
        "chunk_id": chunk_id
    }