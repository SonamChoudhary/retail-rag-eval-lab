# retail-rag-eval-lab

RAG system over retail SEC filings (Walmart, Target, Costco, Kroger) with
RAGAS-based evaluation comparing naive vs. improved retrieval.

## Problem

Retail analysts and investors regularly need answers to specific questions
buried across long, dense SEC filings (10-Ks and 10-Qs) - e.g., comparing
inventory strategy language across competitors, or tracking how a company's
risk factors changed year over year. This project builds a retrieval-augmented
generation (RAG) system to answer natural-language questions grounded in a
real corpus of retail filings, with rigorous evaluation of retrieval and
answer quality rather than just a working demo.

## Corpus

~90 10-K and 10-Q filings (2021-2026) for Walmart (WMT), Target (TGT),
Costco (COST), and Kroger (KR), pulled from SEC EDGAR via
`sec-edgar-downloader`. See `scripts/ingest.py`.

Filing structure notes:
- 10-Ks reach the exhibits section at "Item 15. Exhibits"; 10-Qs reach it
  at "Item 6. Exhibits" - item numbering is not consistent between form types.
- Both form types end with a "SIGNATURES" heading shortly after exhibits.
- Chunking excludes everything from "SIGNATURES" onward as boilerplate.

## Approach
Parse -> chunk (~500 tokens, tiktoken) -> embed (sentence-transformers) -> store in Chroma -> retrieve -> generate answer (Claude, grounded strictly in retrieved context). Retrieval compared naive (semantic-only) vs. hybrid (semantic + BM25, fused via Reciprocal Rank Fusion).

## Results
Metric	Semantic (naive)	Hybrid (semantic + BM25)
Hit Rate@10	70%	80%
Avg Precision@10	15%	18%

RAGAS end-to-end evaluation (faithfulness, answer relevancy, context precision/recall): TBD

## What I'd improve with more time

_TBD_
