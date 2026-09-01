""" Chunk text into overlapping token windows for embedding. """
import tiktoken

ENCODING = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks of roughly 'chunk_size' tokens."""
    tokens = ENCODING.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunks.append(ENCODING.decode(chunk_tokens))
        start += chunk_size - overlap
    
    return chunks


