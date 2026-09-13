"""
faiss_index.py
==============
Vector Store — FAISS Index Operations

Handles creating, saving, loading, and adding to the FAISS index.
"""

import numpy as np
import faiss

from app.config.config import FAISS_INDEX_PATH


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """
    Build a new FAISS IndexFlatIP from a set of embeddings.

    IndexFlatIP = exact inner product search.
    With L2-normalised vectors this equals cosine similarity.

    Args:
        embeddings: float32 numpy array of shape (n, dim).

    Returns:
        Populated FAISS index.
    """
    embeddings = np.array(embeddings, dtype="float32")
    dimension  = embeddings.shape[1]
    index      = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index


def save_index(index: faiss.IndexFlatIP, path: str | None = None) -> None:
    """
    Save a FAISS index to disk.

    Args:
        index: The FAISS index to save.
        path:  File path. Defaults to config FAISS_INDEX_PATH.
    """
    save_path = path or str(FAISS_INDEX_PATH)
    faiss.write_index(index, save_path)
    print(f"   ✓ FAISS index saved → {save_path}")


def load_index(path: str | None = None) -> faiss.IndexFlatIP:
    """
    Load a FAISS index from disk.

    Args:
        path: File path. Defaults to config FAISS_INDEX_PATH.

    Returns:
        Loaded FAISS index.
    """
    load_path = path or str(FAISS_INDEX_PATH)
    index     = faiss.read_index(load_path)
    print(f"   ✓ FAISS index loaded ({index.ntotal:,} vectors)")
    return index