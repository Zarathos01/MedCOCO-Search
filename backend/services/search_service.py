import os
from PIL import Image

from models.medclip_model import medclip
from models.medblip_model import medblip
from db.chroma_client import search_images
from config import TOP_K
from services.upload_service import UPLOAD_DIR


def load_image_from_disk(saved_filename: str) -> Image.Image:
    """Load a PIL image directly from disk."""
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {saved_filename}")
    return Image.open(file_path).convert("RGB")


async def search_and_caption(
    query: str,
    owner_id: str,
    top_k: int = TOP_K,
    server_base_url: str = ""
) -> dict:
    """
    Full pipeline:
    1. Embed text query with MedCLIP
    2. Retrieve top_k most similar images from ChromaDB
    3. Filter results to only include images owned by the current user
    4. Load each image from disk and caption with MedBLIP
    5. Sort highest score first
    """
    # Step 1: Embed query
    query_embedding = medclip.embed_text(query)

    # Step 2: Retrieve from ChromaDB — fetch more than top_k
    # because some results may belong to other users and get filtered out
    retrieved = search_images(query_embedding=query_embedding, top_k=top_k * 5)

    if not retrieved:
        return {"query": query, "results": [], "count": 0}

    # Step 3: Filter by owner_id — only return current user's images
    owned = [
        item for item in retrieved
        if item["metadata"].get("owner_id") == owner_id
    ]

    # Trim to top_k after filtering
    owned = owned[:top_k]

    if not owned:
        return {"query": query, "results": [], "count": 0}

    # Step 4: Caption each retrieved image
    results = []
    for item in owned:
        metadata       = item["metadata"]
        filename       = metadata.get("filename", "unknown")
        saved_filename = metadata.get("saved_filename", "")
        file_url       = f"{server_base_url}/api/v1/files/{saved_filename}"

        try:
            image   = load_image_from_disk(saved_filename)
            caption = medblip.caption(image)
        except Exception as e:
            print(f"[CAPTION ERROR] {saved_filename}: {e}")
            caption = "Caption unavailable"

        results.append({
            "image_id":         item["image_id"],
            "filename":         filename,
            "saved_filename":   saved_filename,
            "file_url":         file_url,
            "similarity_score": item["similarity_score"],
            "caption":          caption
        })

    # Step 5: Sort highest score first
    results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {
        "query":   query,
        "count":   len(results),
        "results": results
    }