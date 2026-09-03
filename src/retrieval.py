"""Retrieve relevant chunks from the Chroma vector store for a given question."""

from pathlib import Path

import chromadb

from src.embeddings import embed_texts

CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "retail_filings"

_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
_collection = _client.get_or_create_collection(COLLECTION_NAME)

def retrieve(question, top_k):
    """Return the top_k most relevant chunks for a given question."""
    query_embedding = embed_texts([question])[0]

    results= _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks=[]
    for i in range(len(results["ids"][0])):
        chunks.append(
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        }
    )
    return chunks
