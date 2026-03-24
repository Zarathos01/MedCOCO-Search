import chromadb
from config import CHROMA_PATH, CHROMA_COLLECTION

# Persistent client — data survives server restarts
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    metadata={"hnsw:space": "cosine"}  # cosine similarity for CLIP embeddings
)


def add_image(image_id: str, embedding: list[float], metadata: dict):
    """Store an image embedding with metadata in ChromaDB."""
    collection.add(
        ids=[image_id],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search_images(query_embedding: list[float], top_k: int) -> list[dict]:
    """Find top_k most similar images to the query embedding."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["metadatas", "distances"]
    )
    items = []
    for i in range(len(results["ids"][0])):
        items.append({
            "image_id": results["ids"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity_score": round(results["distances"][0][i], 4)  # Direct cosine similarity
        })
    return items


def get_all_ids() -> list[str]:
    """Return all stored image IDs."""
    return collection.get()["ids"]


def delete_image(image_id: str):
    """Delete an image from the collection."""
    collection.delete(ids=[image_id])
