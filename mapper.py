def map_indices_to_text(indices, chunks):
    if indices is None or len(indices) == 0:
        return []

    results = []
    
    for idx in indices:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])

    return results