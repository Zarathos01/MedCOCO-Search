from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from core.startup import load_models

app = FastAPI(title='MedCOCO-Search API')

@app.get("/")
def test():
    return {"message": "THIS IS NEW VERSION"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    load_models()