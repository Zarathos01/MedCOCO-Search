from models.medclip_model import encode_text
from db.chroma_client import get_user_collection
from config import TOP_K_RESULTS

def handle_search(user_id, query):

    collection = get_user_collection(user_id)

    text_embedding = encode_text(query)

    results = collection.query(
        query_embeddings=[text_embedding.tolist()],
        n_results=TOP_K_RESULTS
    )

    return results