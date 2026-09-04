"""Full RAGAS evaluation comparing naive (semantic) vs. hybrid retrieval pipelines."""

import json
from pathlib import Path

from datasets import Dataset
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from src.hybrid_retrieval import hybrid_retrieve
from src.pipeline import answer_question
from src.retrieval import retrieve

load_dotenv()

GOLDEN_QUESTIONS_PATH = Path("data/eval/golden_questions.json")
RESULTS_PATH = Path("data/eval/ragas_comparison_results.json")
METRICS = [faithfulness, answer_relevancy, context_precision, context_recall]


def build_ragas_dataset(questions: list[dict], retrieve_fn) -> Dataset:
    """Run the pipeline for each question and format results for RAGAS."""
    questions_list, answers_list, contexts_list, ground_truths_list = [], [], [], []

    for q in questions:
        result = answer_question(q["question"], retrieve_fn=retrieve_fn)
        questions_list.append(q["question"])
        answers_list.append(result["answer"])
        contexts_list.append([c["text"] for c in result["retrieved_chunks"]])
        ground_truths_list.append(q["reference_answer"])

    return Dataset.from_dict(
        {
            "question": questions_list,
            "answer": answers_list,
            "contexts": contexts_list,
            "ground_truth": ground_truths_list,
        }
    )


def main():
    with open(GOLDEN_QUESTIONS_PATH) as f:
        questions = json.load(f)

    embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    print("Running naive (semantic) pipeline...")
    naive_dataset = build_ragas_dataset(questions, retrieve)
    naive_scores = evaluate(naive_dataset, metrics=METRICS, embeddings=embeddings)

    print("Running hybrid pipeline...")
    hybrid_dataset = build_ragas_dataset(questions, hybrid_retrieve)
    hybrid_scores = evaluate(hybrid_dataset, metrics=METRICS, embeddings=embeddings)

    naive_df = naive_scores.to_pandas()
    hybrid_df = hybrid_scores.to_pandas()

    metric_names = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

    print("\n=== RAGAS Comparison (averaged across 10 questions) ===")
    print(f"{'Metric':<20} {'Naive':<10} {'Hybrid':<10}")
    for metric_name in metric_names:
        naive_avg = naive_df[metric_name].mean()
        hybrid_avg = hybrid_df[metric_name].mean()
        print(f"{metric_name:<20} {naive_avg:<10.3f} {hybrid_avg:<10.3f}")

    with open(RESULTS_PATH, "w") as f:
        json.dump(
            {
                "naive": naive_df.to_dict(orient="records"),
                "hybrid": hybrid_df.to_dict(orient="records"),
            },
            f,
            indent=2,
        )
    print(f"\nSaved per-question results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()