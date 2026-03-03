from models.medclip_model import encode_image
from models.medblip_model import generate_caption
from db.chroma_client import get_user_collection

def handle_upload(user_id, image, filename):

    embedding = encode_image(image)
    caption = generate_caption(image)

    collection = get_user_collection(user_id)

    collection.add(
        embeddings=[embedding.tolist()],
        metadatas=[{
            "filename": filename,
            "caption": caption
        }],
        ids=[filename]
    )