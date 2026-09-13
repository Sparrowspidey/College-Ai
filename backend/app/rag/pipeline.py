"""
rag/pipeline.py
===============
RAG Pipeline Orchestrator

Connects all modules into one clean pipeline:
    Question → Embed → Search → Map → Generate → Answer

This is the core brain of College-AI.
"""

import faiss

from app.config.config import TOP_K_RESULTS, SIMILARITY_THRESHOLD
from app.vectorstore.search_engine import search_with_threshold
from app.vectorstore.mapper import map_indices_to_chunks
from app.llm.ollama_client import generate_answer


def run_rag_pipeline(
    query: str,
    index: faiss.IndexFlatIP,
    chunks: list[dict],
    k: int = TOP_K_RESULTS,
) -> dict:
    """
    Execute the full RAG pipeline for a student query.

    Flow:
        Query
          → Embed query to vector
          → Search FAISS for top-k similar chunks
          → Filter by similarity threshold
          → Map indices to chunk text
          → Send context + query to Mistral (Ollama)
          → Return answer + sources

    Args:
        query:  The student's question.
        index:  Loaded FAISS index.
        chunks: Full list of chunk dicts from pickle.
        k:      Number of chunks to retrieve.

    Returns:
        Dict with keys: query, answer, context, scores.
    """

    # Step 1 — Retrieve relevant chunk indices and scores
    indices, scores = search_with_threshold(
        query=query,
        index=index,
        k=k,
        threshold=SIMILARITY_THRESHOLD,
    )

    # Step 2 — If nothing relevant found, return early
    if not indices:
        return {
            "query":   query,
            "answer":  "I couldn't find relevant information about that in the IIIT Kottayam knowledge base.",
            "context": [],
            "scores":  [],
        }

    # Step 3 — Map indices to actual chunk dicts
    context_chunks = map_indices_to_chunks(indices, chunks)

    # Attach scores to chunks for source display
    for chunk, score in zip(context_chunks, scores):
        chunk["score"] = round(score, 4)

    # Step 4 — Generate answer via Ollama/Mistral
    answer = generate_answer(query, context_chunks)

    return {
        "query":   query,
        "answer":  answer,
        "context": context_chunks,
        "scores":  scores,
    }