"""Keyword-based retrieval using BM25."""

import json
from pathlib import Path

from rank_bm25 import BM25Okapi

CHUNKS_PATH = Path("data/processed/chunks.jsonl")

def _load_chunks():
    chunks=[]
    with open(CHUNKS_PATH, encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks

def _tokenize(text):
    """Simple whitespace/lowercase tokenizer for BM25."""
    return text.lower().split()

_chunks= _load_chunks()
_tokenized_corpus =[_tokenize(c['text']) for c in _chunks]
_bm25 = BM25Okapi(_tokenized_corpus)

def bm25_search(query, top_k=10):
    """Return the top_k chunks ranked by BM25 keyword relevance."""
    tokenized_query = _tokenize(query)
    scores = _bm25.get_scores(tokenized_query)

    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    results=[]
    for idx in ranked_indices:
        chunk = _chunks[idx]
        results.append(
            {
                "id": chunk["id"],
                "text": chunk["text"],
                "metadata": {
                    "ticker": chunk["ticker"],
                    "form_type": chunk["form_type"],
                    "source_path": chunk["source_path"],
                    "chunk_index": chunk["chunk_index"],
                },
                "score": scores[idx],
            }
        )
    return results

