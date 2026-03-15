from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core.startup import load_models


# ─── Lifespan (replaces deprecated on_event) ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models when the server starts up."""
    load_models()
    yield
    # Cleanup (if needed) goes here


# ─── App ─────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="MedCOCO-Search API",
    description="Upload medical images, search by text using MedCLIP, get captions via MedBLIP.",
    version="1.0.0",
    lifespan=lifespan
)

# ─── CORS (allow mobile app to connect) ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your mobile app's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ──────────────────────────────────────────────────────────────────────
app.include_router(router, prefix="/api/v1")


# ─── Root ────────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "MedCOCO-Search API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
