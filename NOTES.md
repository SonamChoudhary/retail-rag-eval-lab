# Working Notes

## Retrieval sanity-check findings (naive baseline)

Ticker-level retrieval is strong - all 10 golden questions retrieve chunks
from the correct company (100% accuracy across top-3/top-8 checks).

Filing-level (accession/year) precision is weak for cross-filing/comparison
questions - e.g., q7 and q9's top-8 results didn't include the specific
filings the verified answers actually came from, despite correctly
identifying the right company. Likely cause: recurring boilerplate language
("pricing strategy," "digital fulfillment," "inventory") repeats near-
identically across ~5 years of filings per company, making pure semantic
similarity a weak signal for distinguishing *which year's* filing is most
relevant.

This motivates the retrieval improvement planned for Week 2 (hybrid search
and/or metadata-aware retrieval) rather than relying on naive embedding
similarity alone.


## Plan for retrieval improvement analysis (Week 2)

Before implementing hybrid search, establish a quantitative baseline:
- Run all 10 golden questions through retrieval at a fixed top_k (e.g., 8)
- For each question, check: did the correct source_filing(s) appear in the
  results? At what rank? Record as "hit @ rank N" or "miss"
- Compute filing-level precision@k and recall@k across all 10 questions,
  not just eyeball a few (q1, q3 checked manually on Day 4 - q1 strong,
  q3 weak due to wrong-year filing retrieved)

After implementing the improvement:
- Re-run the identical check with the same 10 questions, same top_k
- Compare hit rate, average rank of correct filing, before vs. after
- Run RAGAS (faithfulness, answer relevancy, context precision/recall) on
  both versions - this becomes the before/after table in the README

Day 4 finding to carry forward: generation layer does NOT hallucinate when
given imperfect context (Costco q3 correctly refused rather than guessing
a wrong number) - meaning any answer-quality improvement after the retrieval
fix should be attributable to better retrieval, not a generation-side change.


## Hybrid search (RRF) results vs. naive semantic baseline

Hit Rate: 70% -> 80%. Avg Precision@10: 15% -> 18%.

Not a uniform win: q1 regressed from hit (semantic rank 9) to miss under
fusion. Root cause: the target filing ranked mediocre in both individual
methods (semantic rank 9, BM25 rank 13) rather than strong in either -
for broad/conceptual questions without a sharp distinctive keyword phrase,
BM25 contributes weak signal that can dilute an already-borderline semantic
ranking rather than reinforce it. RRF rewards consistent moderate
performance across both signals over being the single best match in one -
a real trade-off, not just a tuning bug.

q3 (Costco membership fees) improved (miss -> hit) - BM25 caught the
distinctive "membership fee" phrase that semantic search conflated with
wrong-year filings. q6 (Costco warehouse count) still misses in both
methods - deeper than the fusion method choice, worth investigating
(possibly a chunking issue) before assuming retrieval method is the cause.