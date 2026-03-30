from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


class ImageGenerator:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def generate_caption(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(image, return_tensors="pt")
        output = self.model.generate(**inputs)

        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption

    def answer_question(self, image_path, question):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(image, question, return_tensors="pt")
        output = self.model.generate(**inputs)

        answer = self.processor.decode(output[0], skip_special_tokens=True)
        return answer