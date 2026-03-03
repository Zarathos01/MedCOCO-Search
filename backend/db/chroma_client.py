import chromadb
from config import CHROMA_DB_PATH

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_user_collection(user_id: str):
    return client.get_or_create_collection(
        name=f"user_{user_id}_collection"
    )