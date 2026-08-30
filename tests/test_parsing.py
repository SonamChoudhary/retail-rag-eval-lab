from pathlib import Path
from src.parsing import extract_text

SAMPLE_FILING = Path("data/raw/sec-edgar-filings/WMT/10-Q/0000104169-21-000042/primary-document.html")

def test_extract_text_returns_nonempty_string():
    text = extract_text(SAMPLE_FILING)
    assert isinstance(text,str)
    assert len(text) > 0

def test_extract_text_excludes_signatures_section():
    text = extract_text(SAMPLE_FILING)
    assert "SIGNATURES" not in text.upper()