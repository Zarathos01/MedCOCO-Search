import uuid
import os
from io import BytesIO

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

from models.medclip_model import medclip
from db.chroma_client import add_image, get_all_ids
from config import Config

# ── Upload folder path ────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads")


def try_open_image(contents: bytes) -> Image.Image:
    """Try multiple ways to open image bytes handling corrupted headers."""
    try:
        img = Image.open(BytesIO(contents))
        img.verify()
        return Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        pass

    png_sig = b'\x89PNG\r\n\x1a\n'
    idx = contents.find(png_sig)
    if idx > 0:
        try:
            return Image.open(BytesIO(contents[idx:])).convert("RGB")
        except Exception:
            pass

    jpg_sig = b'\xff\xd8\xff'
    idx = contents.find(jpg_sig)
    if idx > 0:
        try:
            return Image.open(BytesIO(contents[idx:])).convert("RGB")
        except Exception:
            pass

    raise UnidentifiedImageError("Could not open image after multiple attempts.")


def save_file_to_disk(contents: bytes, filename: str) -> str:
    """
    Save image bytes to the uploads folder.
    Creates the folder if it doesn't exist.
    Returns the saved filename with a unique prefix.
    """
    # Always ensure folder exists right before saving
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(filename)[-1].lower() or ".jpg"
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(contents)
    return unique_name


def delete_file_from_disk(saved_filename: str):
    """Delete an image file from the uploads folder."""
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    if os.path.exists(file_path):
        os.remove(file_path)


async def process_upload(files: list[UploadFile], current_user, request) -> dict:
    """
    For each uploaded file:
    1. Read and validate as PIL image
    2. Save raw file to disk
    3. Generate MedCLIP embedding
    4. Store embedding + filename in ChromaDB (no URL — built dynamically at request time)
    """
    results = []
    existing_ids = get_all_ids()

    for file in files:
        contents = await file.read()

        print(f"[UPLOAD] Filename: {file.filename}")
        print(f"[UPLOAD] Size: {len(contents)} bytes")

        if not contents:
            raise ValueError(f"File {file.filename} is empty.")

        # Validate and open image
        try:
            image = try_open_image(contents)
        except Exception as e:
            raise ValueError(f"Could not open {file.filename}: {str(e)}")

        # Save file to disk
        saved_filename = save_file_to_disk(contents, file.filename)

        # Generate MedCLIP embedding
        image_id = str(uuid.uuid4())
        embedding = medclip.embed_image(image)

        # Store in ChromaDB — only filename stored, URL built at request time
        add_image(
            image_id=image_id,
            embedding=embedding,
            metadata={
                "filename": file.filename,
                "saved_filename": saved_filename,
                "owner_id": str(current_user.uid)
            }
        )

        results.append({
            "image_id": image_id,
            "filename": file.filename,
            "saved_filename": saved_filename,
            "status": "uploaded"
        })

    return {
        "uploaded": len(results),
        "total_in_db": len(existing_ids) + len(results),
        "files": results
    }