"""
mapper.py
=========
Vector Store — Index to Text Mapper

Maps FAISS search result indices back to the actual chunk dictionaries.
"""


def map_indices_to_chunks(
    indices: list[int],
    chunks: list[dict],
) -> list[dict]:
    """
    Convert a list of FAISS indices to their corresponding chunk dicts.

    Args:
        indices: List of integer indices from FAISS search results.
        chunks:  Full list of chunk dicts loaded from pickle.

    Returns:
        List of chunk dicts (with text, source, url, type fields).
    """
    if not indices:
        return []

    results = []
    for idx in indices:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])

    return results


def map_indices_to_text(
    indices: list[int],
    chunks: list[dict],
) -> list[str]:
    """
    Convert FAISS indices to plain text strings only.
    Kept for backwards compatibility with older pipeline code.

    Args:
        indices: List of integer indices.
        chunks:  Full list of chunk dicts.

    Returns:
        List of text strings.
    """
    chunk_dicts = map_indices_to_chunks(indices, chunks)
    return [c["text"] for c in chunk_dicts]