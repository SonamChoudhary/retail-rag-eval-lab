"""Generate embeddings for text chunks using a local sentence-transformers model."""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts):
    """Embed a list of text strings into vectors."""
    embeddings = _model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()