from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def search(query, index, k=3):
    query_vector = model.encode([query])
    query_vector = np.array(query_vector, dtype='float32')

    # normalize query vector
    query_vector = query_vector / np.linalg.norm(query_vector, axis=1, keepdims=True)

    D, I = index.search(query_vector, k)

    return I[0].tolist(), D[0].tolist()