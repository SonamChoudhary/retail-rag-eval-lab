from pathlib import Path

import pytest

CHUNKS_PATH = Path("data/processed/chunks.jsonl")

requires_data = pytest.mark.skipif(
    not CHUNKS_PATH.exists(),
    reason="chunks.jsonl not present - run `make process` locally first"
)

@requires_data
def test_hybrid_retrieve_returns_results():
    from src.hybrid_retrieval import hybrid_retrieve

    results = hybrid_retrieve("membership fee", top_k=5)
    assert len(results) == 5
    assert all("metadata" in r for r in results)