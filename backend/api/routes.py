from fastapi import APIRouter, UploadFile, File
from services.upload_service import handle_upload
from services.search_service import handle_search

router = APIRouter()

@router.post("/upload")
async def upload_image(user_id: str, file: UploadFile = File(...)):
    image_bytes = await file.read()
    # preprocess image
    handle_upload(user_id, image_bytes, file.filename)
    return {"message": "Uploaded successfully"}

@router.post("/search")
async def search(user_id: str, query: str):
    results = handle_search(user_id, query)
    return results