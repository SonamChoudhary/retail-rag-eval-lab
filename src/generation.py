"""Generate answers using retrieved context and the Claude API."""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
_client = Anthropic(api_key = os.environ["ANTHROPIC_API_KEY"])

def build_prompt(question, chunks):
    """Build a prompt combining the question with retrieved context."""
    context_blocks=[]

    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"]
        context_blocks.append(
            f"[Source{i+1}]: {meta['ticker']} {meta['form_type']}]\n{chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_blocks) 
    return f"""Answer the question using ONLY the context provided below. If the context doesn't contain enough information to answer, say so explicitly rather than guessing.

Context:
{context}
Question: {question}
Answer:"""

def generate(question, chunks):
    """Generate an answer to the question, grounded in the retrieved chunks """
    prompt = build_prompt(question, chunks)

    response = _client.messages.create(
        model = MODEL,
        max_tokens = 500,
        messages =[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


