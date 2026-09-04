from pathlib import Path

import pytest

CHUNKS_PATH = Path("data/processed/chunks.jsonl")

requires_chunks_data = pytest.mark.skipif(
    not CHUNKS_PATH.exists(),
    reason="chunks.jsonl not present - run `make process` locally first",
)


@requires_chunks_data
def test_bm25_search_returns_results():
    from src.bm25_search import bm25_search
    results = bm25_search("membership fee", top_k=5)
    assert len(results) == 5
    assert all("score" in r for r in results)


@requires_chunks_data
def test_bm25_search_finds_costco_for_membership_query():
    from src.bm25_search import bm25_search
    
    results = bm25_search("membership fee", top_k=10)
    tickers = [r["metadata"]["ticker"] for r in results]
    assert "COST" in tickers