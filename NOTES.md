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