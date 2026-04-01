from PIL import Image
import pytesseract


class ContextualCaptionGenerator:
    def __init__(self, blip_generator, llm):
        self.blip = blip_generator
        self.llm = llm

    def extract_ocr(self, image_path):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except:
            return ""

    def generate(self, image_path):
        # Step 1: BLIP caption
        blip_caption = self.blip.generate_caption(image_path)

        # Step 2: OCR text
        ocr_text = self.extract_ocr(image_path)

        # Step 3: Prompt for LLM
        prompt = f"""
You are an expert at understanding images.

Visual Caption:
{blip_caption}

Extracted Text:
{ocr_text}

Task:
Combine both and generate a meaningful, context-aware description.

Final Caption:
"""

        final_caption = self.llm.generate(prompt)

        return {
            "blip": blip_caption,
            "ocr": ocr_text,
            "final": final_caption.strip()
        }