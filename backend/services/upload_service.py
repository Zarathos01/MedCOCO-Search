import uuid
import base64
import io
from io import BytesIO

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from sqlmodel.ext.asyncio.session import AsyncSession

from models.medclip_model import medclip
from db.chroma_client import add_image, get_all_ids
from db.models import Images


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL image to base64 string for storage in ChromaDB metadata."""
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def try_open_image(contents: bytes) -> Image.Image:
    """
    Try multiple ways to open image bytes.
    Handles corrupted headers and BOM bytes.
    """
    # Try 1: direct open
    try:
        img = Image.open(BytesIO(contents))
        img.verify()
        return Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        pass

    # Try 2: strip leading garbage until PNG header
    png_sig = b'\x89PNG\r\n\x1a\n'
    idx = contents.find(png_sig)
    if idx > 0:
        try:
            return Image.open(BytesIO(contents[idx:])).convert("RGB")
        except Exception:
            pass

    # Try 3: strip leading garbage until JPEG header
    jpg_sig = b'\xff\xd8\xff'
    idx = contents.find(jpg_sig)
    if idx > 0:
        try:
            return Image.open(BytesIO(contents[idx:])).convert("RGB")
        except Exception:
            pass

    # Try 4: decode as base64 in case it was sent encoded
    try:
        decoded = base64.b64decode(contents)
        return Image.open(BytesIO(decoded)).convert("RGB")
    except Exception:
        pass

    raise UnidentifiedImageError("Could not open image after multiple attempts.")


async def process_upload(files: list[UploadFile], current_user, session: AsyncSession) -> dict:
    """
    For each uploaded file:
    1. Read and open as PIL image
    2. Save raw bytes to PostgreSQL (for home page display)
    3. Generate MedCLIP embedding
    4. Store embedding + base64 in ChromaDB (for AI search)
    """
    results = []
    existing_ids = get_all_ids()

    for file in files:
        contents = await file.read()

        print(f"[UPLOAD] Filename: {file.filename}")
        print(f"[UPLOAD] Size: {len(contents)} bytes")
        print(f"[UPLOAD] First bytes: {contents[:12]}")

        if not contents:
            raise ValueError(f"File {file.filename} is empty.")

        # Open and validate the image
        try:
            image = try_open_image(contents)
        except Exception as e:
            raise ValueError(f"Could not open {file.filename}: {str(e)}")

        # ── Step 1: Save raw image to PostgreSQL (home page) ──────────
        db_image = Images(
            filename=file.filename,
            data=contents,
            owner_id=current_user.uid
        )
        session.add(db_image)
        await session.commit()
        await session.refresh(db_image)  # get the auto-generated id

        # ── Step 2: Save embedding to ChromaDB (AI search) ────────────
        image_id = str(db_image.id)     # use PostgreSQL id as ChromaDB id
        embedding = medclip.embed_image(image)
        image_b64 = image_to_base64(image)

        add_image(
            image_id=image_id,
            embedding=embedding,
            metadata={
                "filename": file.filename,
                "image_b64": image_b64,
                "owner_id": str(current_user.uid)
            }
        )

        results.append({
            "image_id": image_id,
            "filename": file.filename,
            "status": "uploaded"
        })

    return {
        "uploaded": len(results),
        "total_in_db": len(existing_ids) + len(results),
        "files": results
    }
