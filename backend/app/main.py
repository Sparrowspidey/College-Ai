"""
main.py
=======
College-AI FastAPI Backend

Endpoints:
    GET  /health   — check if API + resources are loaded
    POST /ask      — submit a question, get an answer

Usage:
    cd backend
    uvicorn app.main:app --reload
"""

import os
import pickle
import sys
import time
from contextlib import asynccontextmanager
from typing import List, Optional

import faiss
import numpy as np
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


# ── Config ───────────────────────────────────────────────────────────────────
EMBEDDING_MODEL      = "all-MiniLM-L6-v2"
OLLAMA_MODEL         = "mistral"
OLLAMA_URL           = "http://localhost:11434/api/generate"
TOP_K                = 5
SIMILARITY_THRESHOLD = 0.30

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "..", "..", "data", "processed")
INDEX_PATH  = os.path.join(DATA_DIR, "faiss_index.index")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks_for_retrieval.pkl")


# ── Global resources (loaded once at startup) ─────────────────────────────────
resources = {
    "index":  None,
    "chunks": None,
    "model":  None,
    "ready":  False,
}


# ── Lifespan: load everything when server starts ──────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 College-AI API starting up...")

    try:
        # Load FAISS index
        if not os.path.exists(INDEX_PATH):
            print(f"❌ ERROR: FAISS index not found at {INDEX_PATH}")
            print("   Run build_index.py first.")
            sys.exit(1)

        resources["index"] = faiss.read_index(INDEX_PATH)
        print(f"   ✓ FAISS index loaded  ({resources['index'].ntotal:,} vectors)")

        # Load chunks
        if not os.path.exists(CHUNKS_PATH):
            print(f"❌ ERROR: Chunks file not found at {CHUNKS_PATH}")
            sys.exit(1)

        with open(CHUNKS_PATH, "rb") as f:
            resources["chunks"] = pickle.load(f)
        print(f"   ✓ Chunks loaded       ({len(resources['chunks']):,} chunks)")

        # Load embedding model
        resources["model"] = SentenceTransformer(EMBEDDING_MODEL)
        print(f"   ✓ Embedding model     ({EMBEDDING_MODEL})")

        resources["ready"] = True
        print("\n✅ College-AI API is ready!\n")

    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

    yield  # API runs here

    print("\n👋 College-AI API shutting down...")


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="College-AI API",
    description="AI-powered assistant for IIIT Kottayam students",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow frontend to call the API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic models ───────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = TOP_K

class SourceItem(BaseModel):
    url: str
    source: str
    score: float

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    time_taken: float


# ── Helper: embed query ───────────────────────────────────────────────────────
def embed_query(query: str) -> np.ndarray:
    model  = resources["model"]
    vector = model.encode([query], convert_to_numpy=True)
    vector = np.array(vector, dtype="float32")
    vector = vector / np.linalg.norm(vector, axis=1, keepdims=True)
    return vector


# ── Helper: search FAISS ──────────────────────────────────────────────────────
def search_chunks(query_vector: np.ndarray, k: int) -> list:
    index  = resources["index"]
    chunks = resources["chunks"]

    scores, indices = index.search(query_vector, k)
    scores  = scores[0].tolist()
    indices = indices[0].tolist()

    results = []
    for score, idx in zip(scores, indices):
        if idx == -1 or score < SIMILARITY_THRESHOLD:
            continue
        chunk = chunks[idx]
        results.append({
            "score":  round(score, 4),
            "text":   chunk["text"],
            "source": chunk.get("source", ""),
            "url":    chunk.get("url", ""),
        })

    return results


# ── Helper: generate answer via Ollama ───────────────────────────────────────
def generate_answer(question: str, context_chunks: list) -> str:
    if not context_chunks:
        return "I couldn't find relevant information about that in the IIIT Kottayam knowledge base."

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

Question: {question}

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
            return response.json().get("response", "No response received.").strip()
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Ollama returned HTTP {response.status_code}"
            )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure it is running: 'ollama serve'"
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama timed out. Try again."
        )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Check if the API and all resources are ready."""
    if not resources["ready"]:
        raise HTTPException(status_code=503, detail="API is not ready yet.")

    return {
        "status":         "ok",
        "vectors_loaded": resources["index"].ntotal,
        "chunks_loaded":  len(resources["chunks"]),
        "model":          EMBEDDING_MODEL,
        "llm":            OLLAMA_MODEL,
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    Submit a question about IIIT Kottayam.
    Returns an answer generated from the college knowledge base.
    """
    if not resources["ready"]:
        raise HTTPException(status_code=503, detail="API is not ready yet.")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.time()

    # Step 1: Embed the question
    query_vector = embed_query(question)

    # Step 2: Retrieve relevant chunks
    relevant_chunks = search_chunks(query_vector, request.top_k)

    # Step 3: Generate answer
    answer = generate_answer(question, relevant_chunks)

    # Step 4: Build unique source list
    seen    = set()
    sources = []
    for chunk in relevant_chunks:
        url = chunk.get("url") or chunk.get("source", "")
        if url and url not in seen:
            sources.append(SourceItem(
                url=url,
                source=chunk.get("source", ""),
                score=chunk["score"],
            ))
            seen.add(url)

    return AskResponse(
        question=question,
        answer=answer,
        sources=sources,
        time_taken=round(time.time() - start, 2),
    )