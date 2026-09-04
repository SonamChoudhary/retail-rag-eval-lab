"""Tests for generation and the end-to-end pipeline."""

import os

import pytest

from src.pipeline import answer_question

requires_api_key = pytest.mark.skipif(
    "ANTHROPIC_API_KEY" not in os.environ,
    reason="ANTHROPIC_API_KEY not set - skipping live API test",
)


@requires_api_key
def test_answer_question_returns_expected_structure():
    result = answer_question("What macroeconomic risks did Walmart identify?")
    assert "question" in result
    assert "answer" in result
    assert "retrieved_chunks" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0