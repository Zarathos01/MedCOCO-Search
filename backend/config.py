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


# import os
# import torch
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     # ─────────────────────────────────────────────
#     # ENV CONFIG
#     # ─────────────────────────────────────────────
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )

#     # ─────────────────────────────────────────────
#     # DATABASE
#     # ─────────────────────────────────────────────
#     DATABASE_URL: str
#     POSTGRES_USER: str = "postgres"
#     POSTGRES_PASSWORD: str = "password"
#     POSTGRES_DB: str = "medcoco"

#     # ─────────────────────────────────────────────
#     # JWT
#     # ─────────────────────────────────────────────
#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str = "HS256"

#     # ─────────────────────────────────────────────
#     # REDIS / CELERY
#     # ─────────────────────────────────────────────
#     REDIS_HOST: str = "localhost"
#     REDIS_PORT: int = 6379
#     REDIS_URL: str = "redis://localhost:6379/0"

#     # Celery (IMPORTANT)
#     broker_url: str = REDIS_URL
#     result_backend: str = REDIS_URL
#     broker_connection_retry_on_startup: bool = True

#     # ─────────────────────────────────────────────
#     # MAIL
#     # ─────────────────────────────────────────────
#     MAIL_USERNAME: str = ""
#     MAIL_PASSWORD: str = ""
#     MAIL_SERVER: str = "smtp.gmail.com"
#     MAIL_PORT: int = 587
#     MAIL_FROM: str = ""
#     MAIL_FROM_NAME: str = "MedCOCO Search"
#     MAIL_STARTTLS: bool = True
#     MAIL_SSL_TLS: bool = False
#     USE_CREDENTIALS: bool = True
#     VALIDATE_CERTS: bool = True

#     # ─────────────────────────────────────────────
#     # APP
#     # ─────────────────────────────────────────────
#     DOMAIN: str = "localhost:8000"

#     # ─────────────────────────────────────────────
#     # AI / STORAGE (computed)
#     # ─────────────────────────────────────────────
#     BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
#     CHROMA_PATH: str = os.path.join(BASE_DIR, "chroma_store")
#     CHROMA_COLLECTION: str = "medical_images"
#     TOP_K: int = 5

#     # ─────────────────────────────────────────────
#     # MODELS
#     # ─────────────────────────────────────────────
#     MEDCLIP_MODEL_NAME: str = "hf-hub:luhuitong/CLIP-ViT-L-14-448px-MedICaT-ROCO"
#     MEDBLIP_MODEL_NAME: str = "WafaaFraih/blip-roco-radiology-captioning"

#     # ─────────────────────────────────────────────
#     # DEVICE
#     # ─────────────────────────────────────────────
#     DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"


# # Global config instance
# Config = Settings()

# import os
# from functools import lru_cache
# from dotenv import load_dotenv
# import torch
# from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()


# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )

#     # DB
#     DATABASE_URL: str

#     # JWT
#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str = "HS256"

#     # Redis / Celery
#     REDIS_URL: str = "redis://localhost:6379/0"

#     # Mail
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_SERVER: str
#     MAIL_PORT: int
#     MAIL_FROM: str
#     MAIL_FROM_NAME: str

#     # App
#     DOMAIN: str

# # # ── AI / ChromaDB settings (not from .env, computed here) ─
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")
# CHROMA_COLLECTION = "medical_images"
# TOP_K = 5

# MEDCLIP_MODEL_NAME = os.getenv("MEDCLIP_MODEL_NAME", "hf-hub:luhuitong/CLIP-ViT-L-14-448px-MedICaT-ROCO")
# MEDBLIP_MODEL_NAME = os.getenv("MEDBLIP_MODEL_NAME", "WafaaFraih/blip-roco-radiology-captioning")
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# @lru_cache()
# def get_settings():
#     return Settings()




# import os
# import torch
# from functools import lru_cache
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from dotenv import load_dotenv

# load_dotenv()


# class Settings(BaseSettings):

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )

#     DATABASE_URL: str
#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str = "HS256"

#     REDIS_URL: str = "redis://localhost:6379/0"

#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_SERVER: str
#     MAIL_PORT: int
#     MAIL_FROM: str
#     MAIL_FROM_NAME: str

#     DOMAIN: str

#     MEDCLIP_MODEL_NAME: str = "hf-hub:luhuitong/CLIP-ViT-L-14-448px-MedICaT-ROCO"
#     MEDBLIP_MODEL_NAME: str = "WafaaFraih/blip-roco-radiology-captioning"

#     DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"


# # ✅ SAFE ACCESS (IMPORTANT FIX)
# @lru_cache()
# def get_settings():
#     return Settings()