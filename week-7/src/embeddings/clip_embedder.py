import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image


class CLIPEmbedder:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def embed_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)

        # 🔥 FORCE EXTRACT TENSOR (handles ALL cases)
        if isinstance(outputs, torch.Tensor):
            features = outputs
        elif hasattr(outputs, "image_embeds"):
            features = outputs.image_embeds
        elif hasattr(outputs, "pooler_output"):
            features = outputs.pooler_output
        else:
            raise ValueError(f"Unexpected output type: {type(outputs)}")

        # ✅ Normalize
        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()

    def embed_text(self, text):
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs)

        if isinstance(outputs, torch.Tensor):
            features = outputs
        elif hasattr(outputs, "text_embeds"):
            features = outputs.text_embeds
        elif hasattr(outputs, "pooler_output"):
            features = outputs.pooler_output
        else:
            raise ValueError(f"Unexpected output type: {type(outputs)}")

        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()