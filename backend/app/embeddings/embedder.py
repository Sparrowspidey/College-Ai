"""
embedder.py
===========
Embeddings Module

Converts text chunks into normalised float32 vectors
using SentenceTransformers (all-MiniLM-L6-v2).
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config.config import EMBEDDING_MODEL

# Load model once at module level — shared across the app
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Return the shared embedding model, loading it on first call."""
    global _model
    if _model is None:
        print(f"   Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def generate_embeddings(chunks: list[str], batch_size: int = 64) -> np.ndarray:
    """
    Convert a list of text strings into normalised float32 vectors.

    Args:
        chunks:     List of text strings to embed.
        batch_size: Number of chunks to process per batch.

    Returns:
        numpy array of shape (len(chunks), 384), L2 normalised.
    """
    model      = get_model()
    embeddings = model.encode(
        chunks,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    embeddings = np.array(embeddings, dtype="float32")

    # L2 normalise — required for cosine similarity with IndexFlatIP
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    embeddings = embeddings / norms

    return embeddings


def embed_query(query: str) -> np.ndarray:
    """
    Embed a single query string into a normalised float32 vector.

    Args:
        query: The user's question.

    Returns:
        numpy array of shape (1, 384), L2 normalised.
    """
    model  = get_model()
    vector = model.encode([query], convert_to_numpy=True)
    vector = np.array(vector, dtype="float32")
    vector = vector / np.linalg.norm(vector, axis=1, keepdims=True)
    return vector