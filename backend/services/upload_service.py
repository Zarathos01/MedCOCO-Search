import uuid
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile

from models.medclip_model import medclip
from db.chroma_client import add_image, get_all_ids


def image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def try_open_image(contents: bytes) -> Image.Image:
    """
    Try multiple ways to open the image bytes.
    Handles corrupted headers, BOM bytes, and encoding issues.
    """
    # Try 1: direct open
    try:
        img = Image.open(BytesIO(contents))
        img.verify()  # verify it's a valid image
        # reopen after verify (verify closes the file)
        return Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        pass

    # Try 2: strip leading garbage bytes until PNG header
    png_sig = b'\x89PNG\r\n\x1a\n'
    idx = contents.find(png_sig)
    if idx > 0:
        try:
            return Image.open(BytesIO(contents[idx:])).convert("RGB")
        except Exception:
            pass

    # Try 3: strip leading garbage bytes until JPEG header
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


async def process_upload(files: list[UploadFile]) -> dict:
    results = []
    existing_ids = get_all_ids()

    for file in files:
        contents = await file.read()

        print(f"[UPLOAD] Filename: {file.filename}")
        print(f"[UPLOAD] Size: {len(contents)} bytes")
        print(f"[UPLOAD] First bytes: {contents[:12]}")

        if not contents:
            raise ValueError(f"File {file.filename} is empty.")

        try:
            image = try_open_image(contents)
        except Exception as e:
            raise ValueError(f"Could not open {file.filename}: {str(e)}")

        image_id = str(uuid.uuid4())
        embedding = medclip.embed_image(image)
        image_b64 = image_to_base64(image)

        metadata = {
            "filename": file.filename,
            "image_b64": image_b64
        }

        add_image(image_id=image_id, embedding=embedding, metadata=metadata)

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