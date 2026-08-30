# retail-rag-eval-lab

RAG system over retail SEC filings (Walmart, Target, Costco, Kroger) with
RAGAS-based evaluation comparing naive vs. improved retrieval.

## Problem

Retail analysts and investors regularly need answers to specific questions
buried across long, dense SEC filings (10-Ks and 10-Qs) — e.g., comparing
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
  at "Item 6. Exhibits" — item numbering is not consistent between form types.
- Both form types end with a "SIGNATURES" heading shortly after exhibits.
- Chunking excludes everything from "SIGNATURES" onward as boilerplate.

## Approach

_TBD - week 1-2 in progress_

## Results

_TBD_

## What I'd improve with more time

_TBD_
