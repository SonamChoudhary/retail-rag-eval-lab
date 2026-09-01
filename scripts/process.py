import json
from pathlib import Path

from src.chunking import chunk_text
from src.parsing import extract_text

RAW_DIR = Path("data/raw/sec-edgar-filings")
OUTPUT_PATH = Path("data/processed/chunks.jsonl")

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        for filing_path in RAW_DIR.glob("*/*/*/primary-document.html"):
            ticker = filing_path.parts[-4]
            form_type = filing_path.parts[-3]

            text = extract_text(filing_path)
            chunks = chunk_text(text)

            for i,chunk in enumerate(chunks):
                record = {
                    "id": f"{ticker}_{form_type}_{filing_path.parent.name}_{i}",
                    "ticker": ticker,
                    "form_type": form_type,
                    "source_path": str(filing_path),
                    "chunk_index": i,
                    "text": chunk
                }
                out_file.write(json.dumps(record) + "\n")
                count+=1
    print(f"Wrote {count} chunks to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
