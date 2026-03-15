import base64
from io import BytesIO
from PIL import Image

from models.medclip_model import medclip
from models.medblip_model import medblip
from db.chroma_client import search_images
from config import TOP_K


def base64_to_image(b64_string: str) -> Image.Image:
    """Convert base64 string back to PIL image."""
    image_data = base64.b64decode(b64_string)
    return Image.open(BytesIO(image_data)).convert("RGB")


async def search_and_caption(query: str, top_k: int = TOP_K) -> dict:
    """
    Full pipeline:
    1. Embed the text query using MedCLIP
    2. Retrieve top_k most similar images from ChromaDB
    3. Caption each retrieved image using MedBLIP
    4. Return results with images + captions + similarity scores
    """
    # Step 1: Embed query
    query_embedding = medclip.embed_text(query)

    # Step 2: Retrieve from ChromaDB
    retrieved = search_images(query_embedding=query_embedding, top_k=top_k)

    if not retrieved:
        return {"query": query, "results": [], "count": 0}

    # Step 3: Caption each retrieved image
    results = []
    for item in retrieved:
        image_b64 = item["metadata"].get("image_b64", "")
        filename = item["metadata"].get("filename", "unknown")

        # Convert stored base64 back to PIL for captioning
        image = base64_to_image(image_b64)
        caption = medblip.caption(image)

        results.append({
            "image_id": item["image_id"],
            "filename": filename,
            "similarity_score": item["similarity_score"],
            "caption": caption,
            "image_b64": image_b64  # mobile app can render this directly
        })

    return {
        "query": query,
        "count": len(results),
        "results": results
    }
