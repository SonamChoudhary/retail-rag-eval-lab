"""End-to-end RAG pipeline: retrieve relevant chunks, then generate an answer."""
from collections.abc import Callable

from src.generation import generate
from src.retrieval import retrieve


def answer_question(question, top_k=5, retrieve_fn: Callable = retrieve):
    """ Run the full RAG pipeline: retrieve context, generate a grounded answer """
    chunks = retrieve_fn(question, top_k=top_k)
    answer= generate(question, chunks)

    return{
        "question": question,
        "answer": answer,
        "retrieved_chunks": chunks
    } 
