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

RAGAS end-to-end evaluation (faithfulness, answer relevancy, context precision/recall) RAGAS end-to-end evaluation (10 golden questions, naive vs. hybrid):

| Metric | Naive | Hybrid |
|---|---|---|
| Faithfulness | 0.88 | 0.87 |
| Answer Relevancy | 0.29 | 0.20 |
| Context Precision | 0.25 | 0.45 |
| Context Recall | 0.30 | 0.45 |

Context precision/recall improvements independently confirm the custom
retrieval metrics from the baseline comparison. Faithfulness stayed stable
(generation doesn't depend on which retrieval method fed it). Answer
relevancy dropped under hybrid - see NOTES.md for why this isn't
necessarily bad news.

## What I'd improve with more time

- Metadata-based year filtering (highest-priority, root-cause-backed). Traced a specific retrieval failure (q6, Costco warehouse count) through chunking -> retrieval -> generation and found the correct chunk was retrieved, just ranked outside the top-k window - crowded out by near-identical "warehouse count" boilerplate from other fiscal years. Fix: extract filing year from the SEC accession number as chunk metadata, detect year mentions in the question, and pre-filter candidates to that year via Chroma's metadata where clause before ranking - removing the cross-year competition entirely rather than trying to out-rank it.
- BM25 stopword filtering - confirmed BM25 is diluted by generic, high-frequency terms ("fiscal," bare years); a filing-specific stopword list would sharpen its contribution to hybrid search.
- Chunk-level date signals - prepending each chunk's filing period directly into its text (not just metadata) before embedding, so the embedding itself - not just Chroma's filter - can distinguish near- duplicate content across years.
- Cross-encoder reranking - a heavier but more accurate alternative to RRF fusion at larger scale, where pre-filtering by metadata alone wouldn't be as cheap or sufficient as it is at this corpus's size (~90 filings).
- A relevancy-aware eval metric - RAGAS's answer relevancy scored transparent, correctly-hedged answers (e.g., "here's what I found, but not the specific fact you asked for") identically to outright failures. Worth a custom metric or judge prompt that credits honest partial answers differently from silent failures.
