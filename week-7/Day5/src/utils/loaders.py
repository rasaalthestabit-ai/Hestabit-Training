import pandas as pd
from docx import Document
from PIL import Image
import pytesseract
import pdfplumber


def load_pdf(file_path):
    docs = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):

                # ✅ Limit pages (avoid long processing)
                if i > 100:
                    print(f"⚠️ Skipping long PDF: {file_path}")
                    break

                text = page.extract_text()

                if text and text.strip():
                    docs.append({
                        "text": text,
                        "page": i + 1,
                        "source": file_path
                    })

    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
        return []

    return docs


def load_csv(file_path):
    df = pd.read_csv(file_path)
    docs = []

    for i, row in df.iterrows():
        docs.append({
            "text": " ".join(map(str, row.values)),
            "page": i,
            "source": file_path
        })

    return docs


def load_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])

    return [{
        "text": text,
        "page": 1,
        "source": file_path
    }]


def load_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        return [{
            "text": text,
            "page": 1,
            "source": file_path
        }]

    except Exception as e:
        print(f"❌ Error reading image {file_path}: {e}")
        return []