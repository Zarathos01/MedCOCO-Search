import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoProcessor
from PIL import Image
from config import MEDBLIP_MODEL_NAME, DEVICE


class MedBLIPModel:
    def __init__(self):
        self.model = None
        self.processor = None

    def load(self):
        print(f"[MedBLIP] Loading model: {MEDBLIP_MODEL_NAME} on {DEVICE}")
        self.processor = AutoProcessor.from_pretrained(MEDBLIP_MODEL_NAME)
        self.model = BlipForConditionalGeneration.from_pretrained(MEDBLIP_MODEL_NAME).to(DEVICE)
        self.model.eval()
        print("[MedBLIP] Model loaded successfully.")

    def caption(self, image: Image.Image) -> str:
        """Generate a caption for a single PIL image."""
        inputs = self.processor(images=image, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=60)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption


# Singleton instance
medblip = MedBLIPModel()
