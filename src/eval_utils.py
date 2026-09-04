"""Shared utilities for evaluating retrieval methods against golden questions."""

from collections.abc import Callable


def accession_from_path(path: str) -> str:
    """Extract the accession number from a filing's source_path."""
    return path.split("/")[-2]


def evaluate_question(question: dict, retrieve_fn: Callable, top_k: int = 10) -> dict:
    """Check whether each expected source filing appears in retrieval results,
    using whichever retrieval function is passed in.
    """
    retrieved = retrieve_fn(question["question"], top_k=top_k)
    retrieved_accessions = [
        accession_from_path(r["metadata"]["source_path"]) for r in retrieved
    ]

    expected_accessions = [
        accession_from_path(p) for p in question["source_filings"]
    ]

    filing_results = []
    for expected in expected_accessions:
        if expected in retrieved_accessions:
            rank = retrieved_accessions.index(expected) + 1
            filing_results.append({"filing": expected, "hit": True, "rank": rank})
        else:
            filing_results.append({"filing": expected, "hit": False, "rank": None})

    correct_chunk_count = sum(
        1 for acc in retrieved_accessions if acc in expected_accessions
    )
    precision_at_k = correct_chunk_count / top_k

    return {
        "id": question["id"],
        "filing_results": filing_results,
        "precision_at_k": precision_at_k,
        "any_hit": any(f["hit"] for f in filing_results),
    }


def aggregate_metrics(results: list[dict]) -> dict:
    """Compute hit rate and average precision across all question results."""
    hit_rate = sum(1 for r in results if r["any_hit"]) / len(results)
    avg_precision = sum(r["precision_at_k"] for r in results) / len(results)
    return {"hit_rate": hit_rate, "avg_precision": avg_precision}