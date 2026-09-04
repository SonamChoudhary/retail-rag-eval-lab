"""Quantitative baseline evaluation of retrieval against golden questions."""
import json
from pathlib import Path

from src.retrieval import retrieve

GOLDEN_QUESTIONS_PATH = Path("data/eval/golden_questions.json")
RESULTS_PATH = Path("data/eval/retrieval_baseline_results.json")
TOP_K =10

def accession_from_path(path):
    """Extract the accession number from the filing's source path. """
    return path.split("/")[-2]

def evaluate_question(question):
    """check whether each expected source filing appears in retrieval results """
    retrieved = retrieve(question["question"], top_k=TOP_K)
    retrieved_accessions = [accession_from_path(r["metadata"]["source_path"]) for r in retrieved]
    expected_accessions = [accession_from_path(p) for p in question["source_filings"]]

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
    precision_at_k = correct_chunk_count / TOP_K

    return {
        "id": question["id"],
        "question": question["question"],
        "filing_results": filing_results,
        "precision_at_k": precision_at_k,
        "any_hit": any(f["hit"] for f in filing_results),
    }

def main():
    with open(GOLDEN_QUESTIONS_PATH) as f:
        questions = json.load(f)

    results = [evaluate_question(q) for q in questions]
    hit_rate = sum(1 for r in results if r["any_hit"]) / len(results)
    avg_precision = sum(r["precision_at_k"] for r in results) / len(results)

    print(f"{'ID':<5} {'Hit?':<6} {'Precision@10':<14} Filing results")
    for r in results:
        hit_str = "YES" if r["any_hit"] else "NO"
        print(f"{r['id']:<5} {hit_str:<6} {r['precision_at_k']:<14.2f} {r['filing_results']}")

    print(f"\nOverall Hit Rate@{TOP_K}: {hit_rate:.1%}")
    print(f"Overall avg Precision@{TOP_K}: {avg_precision:.2%}")

    with open(RESULTS_PATH, "w") as f:
        json.dump(
            {"hit_rate": hit_rate, "avg_precision": avg_precision, "results": results},
            f,
            indent=2,
        )
    print(f"\nSaved detailed results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
