"""Compare semantic-only retrieval against hybrid (semantic + BM25) retrieval."""

import json
from pathlib import Path

from src.eval_utils import aggregate_metrics, evaluate_question
from src.hybrid_retrieval import hybrid_retrieve
from src.retrieval import retrieve

GOLDEN_QUESTIONS_PATH = Path("data/eval/golden_questions.json")
RESULTS_PATH = Path("data/eval/retrieval_comparison_results.json")
TOP_K = 10


def main():
    with open(GOLDEN_QUESTIONS_PATH) as f:
        questions = json.load(f)

    semantic_results = [evaluate_question(q, retrieve, TOP_K) for q in questions]
    hybrid_results = [evaluate_question(q, hybrid_retrieve, TOP_K) for q in questions]

    semantic_metrics = aggregate_metrics(semantic_results)
    hybrid_metrics = aggregate_metrics(hybrid_results)

    print(f"{'ID':<5} {'Semantic Hit':<14} {'Hybrid Hit':<12} {'Sem P@10':<10} {'Hyb P@10':<10}")
    for s, h in zip(semantic_results, hybrid_results):
        print(
            f"{s['id']:<5} "
            f"{'YES' if s['any_hit'] else 'NO':<14} "
            f"{'YES' if h['any_hit'] else 'NO':<12} "
            f"{s['precision_at_k']:<10.2f} "
            f"{h['precision_at_k']:<10.2f}"
        )

    print(f"\n{'Metric':<20} {'Semantic':<12} {'Hybrid':<12}")
    print(f"{'Hit Rate':<20} {semantic_metrics['hit_rate']:<12.1%} {hybrid_metrics['hit_rate']:<12.1%}")
    print(f"{'Avg Precision':<20} {semantic_metrics['avg_precision']:<12.1%} {hybrid_metrics['avg_precision']:<12.1%}")

    with open(RESULTS_PATH, "w") as f:
        json.dump(
            {
                "semantic": {"metrics": semantic_metrics, "results": semantic_results},
                "hybrid": {"metrics": hybrid_metrics, "results": hybrid_results},
            },
            f,
            indent=2,
        )
    print(f"\nSaved detailed comparison to {RESULTS_PATH}")


if __name__ == "__main__":
    main()