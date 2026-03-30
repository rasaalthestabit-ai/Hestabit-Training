import re
import unicodedata


def clean_text(text: str) -> str:
    # ----------------------------
    # 1. Unicode normalization
    # ----------------------------
    text = unicodedata.normalize("NFKC", text)

    # ----------------------------
    # 2. Remove invisible/control chars
    # ----------------------------
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # ----------------------------
    # 3. Fix common OCR / PDF issues
    # ----------------------------
    # Remove hyphenation across line breaks: "exam-\nple" → "example"
    text = re.sub(r'-\n', '', text)

    # Join broken lines within paragraphs
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # ----------------------------
    # 4. Normalize newlines
    # ----------------------------
    text = re.sub(r'\n+', '\n', text)

    # ----------------------------
    # 5. Normalize spaces
    # ----------------------------
    text = re.sub(r'[ \t]+', ' ', text)

    # ----------------------------
    # 6. Fix spacing around punctuation
    # ----------------------------
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)   # remove space before punctuation
    text = re.sub(r'([.,!?;:])(?=\w)', r'\1 ', text)  # ensure space after punctuation

    # ----------------------------
    # 7. Remove repeated punctuation
    # ----------------------------
    text = re.sub(r'([.!?]){2,}', r'\1', text)

    # ----------------------------
    # 8. Optional: remove page numbers (common in PDFs)
    # ----------------------------
    text = re.sub(r'\n\d+\n', '\n', text)

    # ----------------------------
    # 9. Strip leading/trailing whitespace
    # ----------------------------
    return text.strip()