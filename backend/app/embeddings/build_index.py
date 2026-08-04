"""
build_index.py
==============
Pipeline runner: Chunks → Embeddings → FAISS Index

Run this once to build the vector database from the crawled data.
After this runs successfully, the RAG pipeline can answer queries.

Usage:
    cd backend/app/embeddings
    python build_index.py
"""

import os
import pickle
import time

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
CHUNKS_PATH    = os.path.join(BASE_DIR, "..", "..", "..", "data", "processed", "chunks_with_metadata.pkl")
OUTPUT_DIR     = os.path.join(BASE_DIR, "..", "..", "..", "data", "processed")
INDEX_PATH     = os.path.join(OUTPUT_DIR, "faiss_index.index")
CHUNKS_OUT     = os.path.join(OUTPUT_DIR, "chunks_for_retrieval.pkl")

# ── Config ───────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE      = 64     # chunks per batch — increase if you have more RAM


# ── Step 1: Load chunks ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("  College-AI — Vector Index Builder")
print("="*60)

print(f"\n📦 Loading chunks from:\n   {CHUNKS_PATH}")

if not os.path.exists(CHUNKS_PATH):
    print("\n❌ ERROR: chunks_with_metadata.pkl not found!")
    print("   Run chunk.py first to generate it.")
    exit(1)

with open(CHUNKS_PATH, "rb") as f:
    chunks_with_metadata = pickle.load(f)

total_chunks = len(chunks_with_metadata)
print(f"   ✓ Loaded {total_chunks:,} chunks")

# Extract just the text for embedding
texts = [item["text"] for item in chunks_with_metadata]


# ── Step 2: Generate embeddings ──────────────────────────────────────────────
print(f"\n🔢 Generating embeddings...")
print(f"   Model      : {EMBEDDING_MODEL}")
print(f"   Chunks     : {total_chunks:,}")
print(f"   Batch size : {BATCH_SIZE}")
print(f"   (This may take a few minutes on first run — model downloads automatically)\n")

start_time = time.time()

model = SentenceTransformer(EMBEDDING_MODEL)

embeddings = model.encode(
    texts,
    batch_size=BATCH_SIZE,
    show_progress_bar=True,
    convert_to_numpy=True,
)

# Convert to float32 (required by FAISS)
embeddings = np.array(embeddings, dtype="float32")

# Normalize for cosine similarity (works with IndexFlatIP)
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
norms[norms == 0] = 1   # avoid division by zero
embeddings = embeddings / norms

elapsed = time.time() - start_time
print(f"\n   ✓ Embeddings generated in {elapsed:.1f}s")
print(f"   ✓ Shape: {embeddings.shape}  (chunks × dimensions)")


# ── Step 3: Build FAISS index ────────────────────────────────────────────────
print(f"\n🗄  Building FAISS index...")

dimension = embeddings.shape[1]

# IndexFlatIP = exact inner product search
# With normalized vectors this equals cosine similarity
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

print(f"   ✓ Index built")
print(f"   ✓ Vectors stored : {index.ntotal:,}")
print(f"   ✓ Dimensions     : {dimension}")


# ── Step 4: Save everything ──────────────────────────────────────────────────
print(f"\n💾 Saving to disk...")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save FAISS index
faiss.write_index(index, INDEX_PATH)
print(f"   ✓ FAISS index → {INDEX_PATH}")

# Save chunks alongside index so retrieval can map results back to text
with open(CHUNKS_OUT, "wb") as f:
    pickle.dump(chunks_with_metadata, f)
print(f"   ✓ Chunks copy  → {CHUNKS_OUT}")


# ── Done ─────────────────────────────────────────────────────────────────────
print(f"""
{'='*60}
✅ Index build complete!

   Chunks indexed : {index.ntotal:,}
   FAISS index    : faiss_index.index
   Chunks file    : chunks_for_retrieval.pkl
   Time taken     : {elapsed:.1f}s

Next step → run the RAG pipeline to start answering queries.
{'='*60}
""")