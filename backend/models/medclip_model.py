import torch
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from config import MEDCLIP_MODEL_NAME, DEVICE


class MedCLIPModel:
    def __init__(self):
        self.model = None
        self.processor = None

    def load(self):
        print(f"[MedCLIP] Loading model: {MEDCLIP_MODEL_NAME} on {DEVICE}")
        self.model = CLIPModel.from_pretrained(MEDCLIP_MODEL_NAME).to(DEVICE)
        self.processor = CLIPProcessor.from_pretrained(MEDCLIP_MODEL_NAME)
        self.model.eval()

        # Check actual dimensions of both towers
        with torch.no_grad():
            dummy_image = Image.new("RGB", (224, 224))
            img_inputs = self.processor(images=dummy_image, return_tensors="pt").to(DEVICE)
            img_out = self.model.vision_model(**img_inputs)
            self.image_dim = img_out.pooler_output.shape[-1]

            text_inputs = self.processor(text=["test"], return_tensors="pt", padding=True).to(DEVICE)
            txt_out = self.model.text_model(**text_inputs)
            self.text_dim = txt_out.pooler_output.shape[-1]

        print(f"[MedCLIP] Image embedding dim: {self.image_dim}")
        print(f"[MedCLIP] Text embedding dim:  {self.text_dim}")
        print("[MedCLIP] Model loaded successfully.")

    def embed_image(self, image: Image.Image) -> list[float]:
        """Generate 768D embedding for a PIL image."""
        inputs = self.processor(images=image, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = self.model.vision_model(**inputs)
            features = outputs.pooler_output
            features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().cpu().tolist()

    def embed_text(self, text: str) -> list[float]:
        """Generate text embedding and pad it to match image dimension (768D)."""
        inputs = self.processor(
            text=[text], return_tensors="pt", padding=True, truncation=True
        ).to(DEVICE)
        with torch.no_grad():
            outputs = self.model.text_model(**inputs)
            features = outputs.pooler_output
            features = features / features.norm(dim=-1, keepdim=True)

            # Pad text embedding from 512D to 768D to match image embeddings
            if features.shape[-1] < self.image_dim:
                pad_size = self.image_dim - features.shape[-1]
                features = F.pad(features, (0, pad_size))
                features = features / features.norm(dim=-1, keepdim=True)

        return features.squeeze().cpu().tolist()


# Singleton instance
medclip = MedCLIPModel()