from pathlib import Path

from src.parsing import extract_text

SAMPLE_FILING = Path(__file__).parent / "fixtures" / "sample_filing.html"

def test_extract_text_returns_nonempty_string():
    text = extract_text(SAMPLE_FILING)
    assert isinstance(text,str)
    assert len(text) > 0

def test_extract_text_excludes_signatures_section():
    text = extract_text(SAMPLE_FILING)
    assert "SIGNATURES" not in text.upper()