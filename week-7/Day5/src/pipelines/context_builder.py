class ContextBuilder:
    def __init__(self):
        pass

    # ---------------------------
    # DEDUPLICATION
    # ---------------------------
    def deduplicate(self, docs):
        seen = set()
        unique_docs = []

        for doc in docs:
            text = doc["text"]

            if text not in seen:
                seen.add(text)
                unique_docs.append(doc)

        return unique_docs

    # ---------------------------
    # FILTERING (BONUS)
    # ---------------------------
    def apply_filters(self, docs, filters):
        if not filters:
            return docs

        filtered = []

        for doc in docs:
            match = True
            for key, value in filters.items():
                if doc.get(key) != value:
                    match = False
                    break

            if match:
                filtered.append(doc)

        return filtered

    # ---------------------------
    # BUILD FINAL CONTEXT
    # ---------------------------
    def build(self, docs, max_tokens=1000):
        context = ""

        for doc in docs:
            context += f"\n[{doc.get('source')}]\n{doc.get('text')}\n"

            if len(context) > max_tokens:
                break

        return context