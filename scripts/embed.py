import json
from pathlib import Path

import chromadb

from src.embeddings import embed_texts

CHUNKS_PATH = Path("data/processed/chunks.jsonl")
CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "retail_filings"
BATCH_SIZE = 1000

def main():
    chunks=[]
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    print(f"Loaded {len(chunks)} chunks")

    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_embeddings = embeddings[i : i + BATCH_SIZE]
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=batch_embeddings,
            documents=[c["text"] for c in batch],
            metadatas=[
                {
                    "ticker": c["ticker"],
                    "form_type": c["form_type"],
                    "source_path": c["source_path"],
                    "chunk_index": c["chunk_index"],
                }
                for c in batch
            ],
        )
        print(f"  Added batch {i // BATCH_SIZE + 1} ({len(batch)} chunks)")
    print(f"Stored {collection.count()} embeddings in Chroma collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    main()

