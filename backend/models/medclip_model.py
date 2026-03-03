from transformers import AutoModel, AutoProcessor
from config import MEDCLIP_MODEL_NAME

medclip_model = None
processor = None

def load_medclip():
    global medclip_model, processor
    medclip_model = AutoModel.from_pretrained(MEDCLIP_MODEL_NAME)
    processor = AutoProcessor.from_pretrained(MEDCLIP_MODEL_NAME)

def encode_text(text):
    # return embedding vector
    pass

def encode_image(image):
    # return embedding vector
    pass