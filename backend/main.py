from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as ai_router
from auth.routers import auth_router
from core.startup import load_models
from db.sql_main import init_db


# ── Lifespan ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize PostgreSQL tables
    await init_db()
    # 2. Load AI models into RAM
    load_models()
    yield


# ── App ───────────────────────────────────────────────────
app = FastAPI(
    title="MedCOCO-Search API",
    description="Medical image search using MedCLIP + MedBLIP with user authentication.",
    version="2.0.0",
    lifespan=lifespan
)

# ── CORS ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(ai_router,   prefix="/api/v1",      tags=["Images", "Search"])


# ── Root ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "MedCOCO-Search API v2",
        "docs": "/docs",
        "endpoints": {
            "auth":   "/api/v1/auth",
            "upload": "/api/v1/upload",
            "search": "/api/v1/search",
            "health": "/api/v1/health"
        }
    }
