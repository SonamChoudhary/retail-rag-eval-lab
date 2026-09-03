from src.retrieval import retrieve


def test_retrieve_returns_correct_ticker_for_costco_question():
    results = retrieve("What was Costco's total membership fee revenue?", top_k = 3)
    tickers = [r["metadata"]["ticker"] for r in results]
    assert "COST" in tickers

def test_retrieve_returns_results_with_expected_fileds():
    results = retrieve("What was Costco's total membership fee revenue?", top_k = 3)
    assert len(results) == 3
    for r in results:
        assert "text" in r
        assert "metadata" in r
        assert "distance" in r
        
   