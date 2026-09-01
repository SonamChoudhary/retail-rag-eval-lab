from src.chunking import chunk_text


def test_chunk_text_splits_long_text():
    text = "word " * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) > 1

def test_chunk_text_returns_single_chunk_for_short_text():
    text = "short text"
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 1