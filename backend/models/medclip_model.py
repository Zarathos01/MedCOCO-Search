import torch
import torch.nn.functional as F
import open_clip
from PIL import Image
from config import MEDCLIP_MODEL_NAME, DEVICE


class MedCLIPModel:
    def __init__(self):
        self.model = None
        self.preprocess = None
        self.tokenizer = None
        self.image_dim = None

    def load(self):
        print(f"[MedCLIP] Loading model: {MEDCLIP_MODEL_NAME} on {DEVICE}")

        # open_clip loads differently — no CLIPModel/CLIPProcessor
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            MEDCLIP_MODEL_NAME
        )
        self.tokenizer = open_clip.get_tokenizer(MEDCLIP_MODEL_NAME)
        self.model = self.model.to(DEVICE)
        self.model.eval()

        # Detect image embedding dimension
        with torch.no_grad():
            dummy = self.preprocess(Image.new("RGB", (224, 224))).unsqueeze(0).to(DEVICE)
            features = self.model.encode_image(dummy)
            self.image_dim = features.shape[-1]

        print(f"[MedCLIP] Image embedding dim: {self.image_dim}")
        print("[MedCLIP] Model loaded successfully.")

    def embed_image(self, image: Image.Image) -> list[float]:
        """Generate embedding for a PIL image."""
        tensor = self.preprocess(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            features = self.model.encode_image(tensor)
            features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().cpu().tolist()

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a text query and match image dimension."""
        tokens = self.tokenizer([text]).to(DEVICE)
        with torch.no_grad():
            features = self.model.encode_text(tokens)
            features = features / features.norm(dim=-1, keepdim=True)

            # Pad if text dim doesn't match image dim
            if features.shape[-1] < self.image_dim:
                pad_size = self.image_dim - features.shape[-1]
                features = F.pad(features, (0, pad_size))
                features = features / features.norm(dim=-1, keepdim=True)

        return features.squeeze().cpu().tolist()


# Singleton instance
medclip = MedCLIPModel()