from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from services.upload_service import process_upload
from services.search_service import search_and_caption
from db.chroma_client import get_all_ids, delete_image
from config import TOP_K

router = APIRouter()


# ─── Request / Response Schemas ────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = TOP_K


# ─── Health Check ───────────────────────────────────────────────────────────────

@router.get("/health", tags=["Health"])
def health_check():
    """Check if the server is running."""
    return {"status": "ok", "message": "MedCOCO-Search API is running"}


# ─── Upload ─────────────────────────────────────────────────────────────────────

@router.post("/upload", tags=["Images"])
async def upload_images(files: List[UploadFile] = File(description="Upload one or more medical images")):
    """
    Upload one or more medical images.
    Each image is embedded using MedCLIP and stored in ChromaDB.
    
    - Accepts: multipart/form-data with field name 'files'
    - Returns: list of uploaded image IDs and filenames
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    # Validate file types
    for file in files:
        filename: str = file.filename.lower()
        if not filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file: {file.filename}. Use JPEG or PNG."
            )

    try:
        result = await process_upload(files)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ─── Search ─────────────────────────────────────────────────────────────────────

@router.post("/search", tags=["Search"])
async def search(request: SearchRequest):
    """
    Search for medical images using a text query.
    
    Pipeline:
    1. Embeds the query with MedCLIP
    2. Retrieves most similar images from ChromaDB
    3. Captions each image with MedBLIP
    
    - Body: { "query": "chest x-ray with pneumonia", "top_k": 5 }
    - Returns: list of matched images with captions and similarity scores
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    top_k = max(1, min(request.top_k, 20))  # clamp between 1 and 20

    try:
        result = await search_and_caption(query=request.query, top_k=top_k)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# ─── Database Info ───────────────────────────────────────────────────────────────

@router.get("/images", tags=["Images"])
def list_images():
    """Return all image IDs currently stored in the database."""
    ids = get_all_ids()
    return {"total": len(ids), "image_ids": ids}


@router.delete("/images/{image_id}", tags=["Images"])
def remove_image(image_id: str):
    """Delete a specific image from the database by its ID."""
    try:
        delete_image(image_id)
        return {"deleted": image_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
