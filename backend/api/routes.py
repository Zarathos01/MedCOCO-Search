import os
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from services.upload_service import process_upload, delete_file_from_disk, UPLOAD_DIR
from services.search_service import search_and_caption
from db.chroma_client import get_all_ids, delete_image, get_image_metadata
from db.models import Users
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


# ── File serving ──────────────────────────────────────────
@router.get("/files/{filename}", tags=["Files"])
def serve_file(filename: str):
    """Serve an uploaded image file by filename."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


# ── Upload ────────────────────────────────────────────────
@router.post("/upload", tags=["Images"])
async def upload_images(
    request: Request,
    files: List[UploadFile] = File(...),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Upload medical images.
    Saves files to disk and stores embeddings in ChromaDB tagged with owner_id.
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
        result = await process_upload(files, current_user)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ── Search ────────────────────────────────────────────────
@router.post("/search", tags=["Search"])
async def search(
    request: Request,
    body: SearchRequest,
    current_user: Users = Depends(get_current_user)
):
    """
    Search medical images by text query.
    Only returns images uploaded by the currently logged-in user.
    """
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    top_k = max(1, min(body.top_k, 20))
    server_base_url = str(request.base_url).rstrip("/")

    try:
        result = await search_and_caption(
            query=body.query,
            owner_id=str(current_user.uid),   # ← filter by current user
            top_k=top_k,
            server_base_url=server_base_url
        )
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# ── My Images (home page) ─────────────────────────────────
@router.get("/my-images", tags=["Images"])
def get_my_images(
    request: Request,
    current_user: Users = Depends(get_current_user)
):
    """
    Returns all images uploaded by the logged-in user.
    URL is built dynamically from the current request.
    """
    server_base_url = str(request.base_url).rstrip("/")
    all_ids = get_all_ids()
    my_images = []

    for image_id in all_ids:
        meta = get_image_metadata(image_id)
        if meta and meta.get("owner_id") == str(current_user.uid):
            saved_filename = meta.get("saved_filename", "")
            my_images.append({
                "image_id":       image_id,
                "filename":       meta.get("filename", "unknown"),
                "saved_filename": saved_filename,
                "file_url":       f"{server_base_url}/api/v1/files/{saved_filename}"
            })

    return {"total": len(my_images), "images": my_images}


# ── Delete single image ───────────────────────────────────
@router.delete("/images/{image_id}", tags=["Images"])
def remove_image(
    image_id: str,
    current_user: Users = Depends(get_current_user)
):
    """Delete a single image from disk and ChromaDB. Only owner can delete."""
    try:
        meta = get_image_metadata(image_id)
        if meta:
            if meta.get("owner_id") != str(current_user.uid):
                raise HTTPException(status_code=403, detail="Not your image.")
            saved_filename = meta.get("saved_filename", "")
            if saved_filename:
                delete_file_from_disk(saved_filename)

        delete_image(image_id)
        return {"deleted": image_id, "status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


# ── Reset all images ──────────────────────────────────────
@router.delete("/reset", tags=["Images"])
def reset_all(current_user: Users = Depends(get_current_user)):
    """Delete ALL images belonging to the current user from disk and ChromaDB."""
    all_ids = get_all_ids()
    deleted_count = 0

    for image_id in all_ids:
        meta = get_image_metadata(image_id)
        if meta and meta.get("owner_id") == str(current_user.uid):
            saved_filename = meta.get("saved_filename", "")
            if saved_filename:
                delete_file_from_disk(saved_filename)
            delete_image(image_id)
            deleted_count += 1

    return {
        "message": "All your images deleted successfully",
        "deleted": deleted_count
    }


# ── List current user's ChromaDB IDs ─────────────────────
@router.get("/images", tags=["Images"])
def list_images(current_user: Users = Depends(get_current_user)):
    """List image IDs in ChromaDB belonging to the current user only."""
    all_ids = get_all_ids()
    my_ids = []

    for image_id in all_ids:
        meta = get_image_metadata(image_id)
        if meta and meta.get("owner_id") == str(current_user.uid):
            my_ids.append(image_id)

    return {"total": len(my_ids), "image_ids": my_ids}