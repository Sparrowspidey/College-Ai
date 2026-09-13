"""
search_engine.py
================
Vector Store — Similarity Search

Searches the FAISS index using an embedded query vector
and returns the top-k most similar chunk indices and scores.
"""

import numpy as np
import faiss

from app.config.config import TOP_K_RESULTS, SIMILARITY_THRESHOLD
from app.embeddings.embedder import embed_query


def search(
    query: str,
    index: faiss.IndexFlatIP,
    k: int = TOP_K_RESULTS,
) -> tuple[list[int], list[float]]:
    """
    Search the FAISS index for chunks most similar to the query.

    Args:
        query: User's question string.
        index: Loaded FAISS index.
        k:     Number of results to return.

    Returns:
        Tuple of (indices, scores) — both lists of length k.
    """
    query_vector = embed_query(query)
    scores, indices = index.search(query_vector, k)

    return indices[0].tolist(), scores[0].tolist()


def search_with_threshold(
    query: str,
    index: faiss.IndexFlatIP,
    k: int = TOP_K_RESULTS,
    threshold: float = SIMILARITY_THRESHOLD,
) -> tuple[list[int], list[float]]:
    """
    Search and filter results below the similarity threshold.

    Returns only results with score >= threshold.
    Prevents low-quality context from reaching the LLM.
    """
    indices, scores = search(query, index, k)

    filtered_indices = []
    filtered_scores  = []

    for idx, score in zip(indices, scores):
        if idx != -1 and score >= threshold:
            filtered_indices.append(idx)
            filtered_scores.append(score)

    return filtered_indices, filtered_scores