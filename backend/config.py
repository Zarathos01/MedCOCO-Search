import os
import torch
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "medcoco"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_FROM: str = ""
    MAIL_FROM_NAME: str = "MedCOCO Search"
    
    BASE_URL: str = ""  # leave empty for local, set to ngrok/domain in production

    DOMAIN: str = "localhost:8000"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Single instance used everywhere
Config = get_settings()

# AI / ChromaDB settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")
CHROMA_COLLECTION = "medical_images"
TOP_K = 5

MEDCLIP_MODEL_NAME = os.getenv("MEDCLIP_MODEL_NAME", "hf-hub:luhuitong/CLIP-ViT-L-14-448px-MedICaT-ROCO")
MEDBLIP_MODEL_NAME = os.getenv("MEDBLIP_MODEL_NAME", "WafaaFraih/blip-roco-radiology-captioning")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


