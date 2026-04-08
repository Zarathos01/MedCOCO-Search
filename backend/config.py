import os
import torch
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # ── Database ──────────────────────────────────────────
    DATABASE_URL: str
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "medcoco"

    # ── JWT ───────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # ── Redis ─────────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Mail ──────────────────────────────────────────────
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_FROM: str = ""
    MAIL_FROM_NAME: str = "MedCOCO Search"

    # ── App ───────────────────────────────────────────────
    DOMAIN: str = "localhost:8000"


Config = Settings()

# ── AI / ChromaDB settings (not from .env, computed here) ─
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")
CHROMA_COLLECTION = "medical_images"
TOP_K = 5

MEDCLIP_MODEL_NAME = os.getenv("MEDCLIP_MODEL_NAME", "hf-hub:luhuitong/CLIP-ViT-L-14-448px-MedICaT-ROCO")
MEDBLIP_MODEL_NAME = os.getenv("MEDBLIP_MODEL_NAME", "WafaaFraih/blip-roco-radiology-captioning")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
