import base64
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from services.upload_service import process_upload
from services.search_service import search_and_caption
from db.chroma_client import get_all_ids, delete_image
from db.models import Users, Images
from db.sql_main import get_session
from auth.dependencies import get_current_user
from config import TOP_K

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str
    top_k: int = TOP_K


# ── Health ────────────────────────────────────────────────
@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "MedCOCO-Search API is running"}


# ── Upload ────────────────────────────────────────────────
@router.post("/upload", tags=["Images"])
async def upload_images(
    files: List[UploadFile] = File(...),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Upload medical images. Requires a valid access token.
    Saves raw image to PostgreSQL (home page) and
    embedding to ChromaDB (AI search).
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    for file in files:
        if not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file: {file.filename}. Use JPEG or PNG."
            )

    try:
        result = await process_upload(files, current_user, session)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ── Search ────────────────────────────────────────────────
@router.post("/search", tags=["Search"])
async def search(
    request: SearchRequest,
    current_user: Users = Depends(get_current_user)
):
    """
    Search medical images by text query.
    Returns top matches with MedBLIP captions.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    top_k = max(1, min(request.top_k, 20))

    try:
        result = await search_and_caption(query=request.query, top_k=top_k)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# ── Home page images ──────────────────────────────────────
@router.get("/my-images", tags=["Images"])
async def get_my_images(
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Returns all images uploaded by the logged-in user.
    Used to populate the mobile app home page.
    """
    result = await session.exec(
        select(Images).where(Images.owner_id == current_user.uid)
    )
    images = result.all()

    return {
        "total": len(images),
        "images": [
            {
                "id": img.id,
                "filename": img.filename,
                "image_b64": base64.b64encode(img.data).decode("utf-8")
            }
            for img in images
        ]
    }


# ── ChromaDB list / delete ────────────────────────────────
@router.get("/images", tags=["Images"])
def list_images(current_user: Users = Depends(get_current_user)):
    """List all image IDs stored in ChromaDB."""
    ids = get_all_ids()
    return {"total": len(ids), "image_ids": ids}


@router.delete("/images/{image_id}", tags=["Images"])
async def remove_image(
    image_id: str,
    current_user: Users = Depends(get_current_user)
):
    """Delete an image from ChromaDB by ID."""
    try:
        delete_image(image_id)
        return {"deleted": image_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
