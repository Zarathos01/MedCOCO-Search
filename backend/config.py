import os

# Base directory = backend/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ChromaDB will persist here
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")

# Collection name inside ChromaDB
CHROMA_COLLECTION = "medical_images"

# How many images to retrieve per search
TOP_K = 5

# MedCLIP model
MEDCLIP_MODEL_NAME = "ZiyueWang/med-clip"

# MedBLIP model
MEDBLIP_MODEL_NAME = "WafaaFraih/blip-roco-radiology-captioning"

# Device: "cuda" if GPU available, else "cpu"
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
