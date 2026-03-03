from transformers import BlipForConditionalGeneration, AutoProcessor
from config import MEDBLIP_MODEL_NAME

medblip_model = None
processor = None

def load_medblip():
    global medblip_model, processor
    medblip_model = BlipForConditionalGeneration.from_pretrained(MEDBLIP_MODEL_NAME)
    processor = AutoProcessor.from_pretrained(MEDBLIP_MODEL_NAME)

def generate_caption(image):
    # return caption string
    pass