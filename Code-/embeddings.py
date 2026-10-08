"""Embedding model is loaded only when indexing/search is requested."""
from .config import EMBEDDING_MODEL

class Embedder:
    def __init__(self, model_name=EMBEDDING_MODEL):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except Exception as exc:
            raise RuntimeError("Embedding model could not be loaded. Check internet access on first run and install requirements.") from exc
    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()
