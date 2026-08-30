"""Download SEC 10-K and 10-Q filings for the retail RAG corpus."""
import os
from pathlib import Path
from dotenv import load_dotenv
from sec_edgar_downloader import Downloader 
load_dotenv()

TICKERS = ["WMT","TGT", "cost","KR"]
FROM_TYPES = ["10-K", "10-Q"]
AFTER_DATE = "2021-01-01"
DOWNLOAD_DIR = Path("data/raw")

COMPANY_NAME = "retail-rag-eval-lab"
EMAIL = os.environ["SEC_EDGAR_EMAIL"]

def main():
    dl = Downloader(COMPANY_NAME, EMAIL, str(DOWNLOAD_DIR))
    for ticker in TICKERS:
        for form in FROM_TYPES:
            print(f"Downloading {form} filings for {ticker}...")
            dl.get(form, ticker, after = AFTER_DATE, download_details = True)

if __name__ == "__main__":
    main()
