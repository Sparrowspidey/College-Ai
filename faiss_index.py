import faiss
import numpy as np

def create_faiss_index(embeddings):
    embeddings = np.array(embeddings, dtype='float32')
    
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatIP(dimension)  # cosine similarity (with normalized vectors)
    index.add(embeddings)
    
    return index

def save_index(index, path):
    faiss.write_index(index, path)

def load_index(path):
    return faiss.read_index(path)