from pathlib import Path
import chromadb
from .config import VECTOR_DB_DIR

class VectorStore:
    def __init__(self):
        VECTOR_DB_DIR.mkdir(exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection("hld_chunks", metadata={"hnsw:space": "cosine"})
    def rebuild(self, chunks, embeddings):
        try:
            self.client.delete_collection("hld_chunks")
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection("hld_chunks", metadata={"hnsw:space": "cosine"})
        self.collection.add(ids=[c["chunk_id"] for c in chunks], documents=[c["text"] for c in chunks],
            metadatas=[{k: str(v) for k,v in c.items() if k != "text"} for c in chunks], embeddings=embeddings)
    def search(self, embedding, top_k):
        if self.collection.count() == 0: return []
        raw = self.collection.query(query_embeddings=[embedding], n_results=min(top_k, self.collection.count()), include=["documents", "metadatas", "distances"])
        return [{"text": d, **m, "distance": dist} for d,m,dist in zip(raw["documents"][0], raw["metadatas"][0], raw["distances"][0])]
    def count(self): return self.collection.count()
