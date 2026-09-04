"""Hybrid retrieval combining semantic search and BM25 via reciprocal rank fusion."""
from src.bm25_search import bm25_search
from src.retrieval import retrieve

RRF_K=60

def hybrid_retrieve(query, top_k=10, candidate_pool=15):
    """Combine semantic search and BM25 results using reciprocal rank fusion."""

    semantic_results = retrieve(query, top_k=candidate_pool)
    keyword_results = bm25_search(query, top_k=candidate_pool)

    scores, chunk_lookup={}, {}

    for rank, chunk in enumerate(semantic_results, start=1):
        scores[chunk["id"]] = scores.get(chunk["id"], 0) + 1 / (RRF_K + rank)
        chunk_lookup[chunk["id"]] = chunk
    
    for rank, chunk in enumerate(keyword_results, start=1):
        scores[chunk["id"]] = scores.get(chunk["id"], 0) + 1 / (RRF_K + rank)
        chunk_lookup[chunk["id"]] = chunk
    
    ranked_ids = sorted(scores, key=lambda cid:scores[cid], reverse=True)[:top_k]

    return [chunk_lookup[cid] for cid in ranked_ids]