"""
RAG PIPELINE ORCHESTRATOR
(This file controls the flow of the RAG system)
"""

from typing import List

from .search_engine import search
from .mapper import map_indices_to_text

SIMILARITY_THRESHOLD = 0.60

def generate_answer(query: str, context_chunks: List[str]) -> str:
    """
    Placeholder function for LLM response generation.

    The chatbot should respond only using retrieved
    college knowledge base context.
    """

    if not context_chunks:
        return "No relevant information found in the college knowledge base."

    return "Generation module not integrated yet."

def run_rag_pipeline(
    query: str,
    index,
    chunks: List[str]
) -> dict:
    """
    Executes the high-level RAG pipeline.

    Flow:
    Query
      -> Vector Search
      -> Similarity Validation
      -> Context Mapping
      -> Response Generation
    """

    # Step 1 — Retrieve similar chunk indexes and scores
    indices, scores = search(query, index)

    # Step 2 — Prevent hallucination using similarity threshold
    if not scores or scores[0] < SIMILARITY_THRESHOLD:
        return {
            "query": query,
            "context": [],
            "answer": "No relevant information found in the college Database."
        }

    # Step 3 — Convert indexes into actual text chunks
    context_chunks = map_indices_to_text(indices, chunks)

    # Step 4 — Generate response
    answer = generate_answer(query, context_chunks)

    return {
        "query": query,
        "context": context_chunks,
        "scores": scores,
        "answer": answer
    }