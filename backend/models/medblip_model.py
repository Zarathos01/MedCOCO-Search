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
        inputs = self.processor(images=image, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=80,        # slightly longer for medical detail
                min_length=20,             # ensure meaningful minimum length
                num_beams=5,               # better quality beam search
                length_penalty=1.2,        # encourage slightly longer captions
                repetition_penalty=1.3,    # stronger repetition prevention
                no_repeat_ngram_size=3,    # keep 3-gram constraint
                early_stopping=True,
                temperature=1.0,           # keep default — don't add randomness
            )
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption


# Singleton instance
medblip = MedBLIPModel()
