"""
query.py
========
College-AI RAG Pipeline — Terminal Query Interface

Tests the full pipeline end to end:
    Question → Embedding → FAISS Search → Ollama/Mistral → Answer

Usage:
    cd backend/app/rag
    python query.py
"""

import os
import sys
import pickle
import time

import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer


# ── Config ───────────────────────────────────────────────────────────────────
EMBEDDING_MODEL     = "all-MiniLM-L6-v2"
OLLAMA_MODEL        = "mistral"
OLLAMA_URL          = "http://localhost:11434/api/generate"
TOP_K               = 5       # number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.30   # minimum score to be considered relevant

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR     = os.path.join(BASE_DIR, "..", "..", "..", "data", "processed")
INDEX_PATH   = os.path.join(DATA_DIR, "faiss_index.index")
CHUNKS_PATH  = os.path.join(DATA_DIR, "chunks_for_retrieval.pkl")


# ── Load resources (once at startup) ─────────────────────────────────────────
def load_resources():
    print("\n🔄 Loading resources...")

    # Check files exist
    if not os.path.exists(INDEX_PATH):
        print("❌ ERROR: faiss_index.index not found!")
        print("   Run build_index.py first.")
        sys.exit(1)

    if not os.path.exists(CHUNKS_PATH):
        print("❌ ERROR: chunks_for_retrieval.pkl not found!")
        print("   Run build_index.py first.")
        sys.exit(1)

    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)
    print(f"   ✓ FAISS index loaded  ({index.ntotal:,} vectors)")

    # Load chunks
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"   ✓ Chunks loaded       ({len(chunks):,} chunks)")

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"   ✓ Embedding model     ({EMBEDDING_MODEL})")

    return index, chunks, model


# ── Step 1: Embed the query ───────────────────────────────────────────────────
def embed_query(query: str, model) -> np.ndarray:
    vector = model.encode([query], convert_to_numpy=True)
    vector = np.array(vector, dtype="float32")
    # Normalize for cosine similarity
    vector = vector / np.linalg.norm(vector, axis=1, keepdims=True)
    return vector


# ── Step 2: Search FAISS ──────────────────────────────────────────────────────
def search_index(query_vector: np.ndarray, index, chunks: list, k: int = TOP_K):
    scores, indices = index.search(query_vector, k)

    scores  = scores[0].tolist()
    indices = indices[0].tolist()

    results = []
    for score, idx in zip(scores, indices):
        if idx == -1:
            continue
        results.append({
            "score":  score,
            "text":   chunks[idx]["text"],
            "source": chunks[idx].get("source", "unknown"),
            "url":    chunks[idx].get("url", ""),
            "type":   chunks[idx].get("type", ""),
        })

    return results


# ── Step 3: Generate answer via Ollama ───────────────────────────────────────
def generate_answer(query: str, context_chunks: list) -> str:
    # Build context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        source = chunk.get("url") or chunk.get("source", "")
        context_parts.append(f"[{i}] {chunk['text']}\nSource: {source}")

    context = "\n\n".join(context_parts)

    prompt = f"""You are College-AI, a helpful assistant for students of IIIT Kottayam.
Answer the question using ONLY the context provided below.
If the context does not contain enough information to answer, say so clearly.
Do not make up or guess any information.
Keep your answer clear, accurate, and student-friendly.

Context:
{context}

Question: {query}

Answer:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model":  OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"❌ Ollama error: HTTP {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama. Make sure it's running: 'ollama serve'"
    except requests.exceptions.Timeout:
        return "❌ Ollama timed out. Try again."
    except Exception as e:
        return f"❌ Error: {e}"


# ── Full RAG Pipeline ─────────────────────────────────────────────────────────
def run_rag(query: str, index, chunks: list, model) -> dict:
    # Step 1: Embed query
    query_vector = embed_query(query, model)

    # Step 2: Retrieve relevant chunks
    results = search_index(query_vector, index, chunks)

    # Step 3: Filter by similarity threshold
    relevant = [r for r in results if r["score"] >= SIMILARITY_THRESHOLD]

    if not relevant:
        return {
            "query":   query,
            "answer":  "I couldn't find relevant information about that in the IIIT Kottayam knowledge base.",
            "chunks":  [],
            "scores":  [],
        }

    # Step 4: Generate answer
    answer = generate_answer(query, relevant)

    return {
        "query":   query,
        "answer":  answer,
        "chunks":  relevant,
        "scores":  [r["score"] for r in relevant],
    }


# ── Terminal Interface ────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  College-AI — RAG Query Terminal")
    print("  Ask anything about IIIT Kottayam!")
    print("  Type 'quit' or 'exit' to stop.")
    print("=" * 60)

    index, chunks, model = load_resources()

    print("\n✅ Ready! Ask your question.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("\n🔍 Searching knowledge base...")
        start = time.time()

        result = run_rag(query, index, chunks, model)

        elapsed = time.time() - start

        print(f"\n🤖 College-AI:\n{result['answer']}")

        # Show sources
        if result["chunks"]:
            print(f"\n📚 Sources ({len(result['chunks'])} chunks, {elapsed:.1f}s):")
            seen_sources = set()
            for chunk in result["chunks"]:
                source = chunk.get("url") or chunk.get("source", "")
                if source and source not in seen_sources:
                    print(f"   • {source}  (score: {chunk['score']:.3f})")
                    seen_sources.add(source)

        print()


if __name__ == "__main__":
    main()