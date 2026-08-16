"""
main.py
=======
College-AI FastAPI Backend — Entry Point

Endpoints:
    GET  /health   — API status + resource check
    POST /ask      — Submit a question, get an answer

Usage:
    cd backend
    uvicorn app.main:app --reload
"""

import pickle
import sys
import time
from contextlib import asynccontextmanager
from typing import List, Optional

import faiss
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config.config import (
    FAISS_INDEX_PATH, CHUNKS_PATH,
    EMBEDDING_MODEL, LLM_MODEL, TOP_K_RESULTS
)
from app.vectorstore.faiss_index import load_index
from app.rag.pipeline import run_rag_pipeline
from app.llm.ollama_client import check_ollama_health


# ── Global resources ──────────────────────────────────────────────────────
resources: dict = {
    "index":  None,
    "chunks": None,
    "ready":  False,
}


# ── Startup / Shutdown ────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 College-AI API starting up...")

    try:
        if not FAISS_INDEX_PATH.exists():
            print(f"❌ FAISS index not found: {FAISS_INDEX_PATH}")
            print("   Run build_index.py first.")
            sys.exit(1)

        if not CHUNKS_PATH.exists():
            print(f"❌ Chunks file not found: {CHUNKS_PATH}")
            print("   Run build_index.py first.")
            sys.exit(1)

        resources["index"] = load_index()

        with open(CHUNKS_PATH, "rb") as f:
            resources["chunks"] = pickle.load(f)
        print(f"   ✓ Chunks loaded       ({len(resources['chunks']):,} chunks)")

        # Trigger embedding model load
        from app.embeddings.embedder import get_model
        get_model()
        print(f"   ✓ Embedding model     ({EMBEDDING_MODEL})")

        resources["ready"] = True
        print("\n✅ College-AI API is ready!\n")

    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

    yield

    print("\n👋 College-AI API shutting down...")


# ── FastAPI app ───────────────────────────────────────────────────────────
app = FastAPI(
    title="College-AI API",
    description="AI-powered assistant for IIIT Kottayam students",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic models ───────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = TOP_K_RESULTS


class SourceItem(BaseModel):
    url: str
    source: str
    score: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    time_taken: float


# ── Routes ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    """Check API status and resource availability."""
    if not resources["ready"]:
        raise HTTPException(status_code=503, detail="API not ready.")

    return {
        "status":         "ok",
        "vectors_loaded": resources["index"].ntotal,
        "chunks_loaded":  len(resources["chunks"]),
        "embedding_model": EMBEDDING_MODEL,
        "llm_model":      LLM_MODEL,
        "ollama_running": check_ollama_health(),
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """Submit a question about IIIT Kottayam and receive an AI answer."""
    if not resources["ready"]:
        raise HTTPException(status_code=503, detail="API not ready.")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.time()

    result = run_rag_pipeline(
        query=question,
        index=resources["index"],
        chunks=resources["chunks"],
        k=request.top_k,
    )

    # Build unique source list
    seen    = set()
    sources = []
    for chunk in result["context"]:
        url = chunk.get("url") or chunk.get("source", "")
        if url and url not in seen:
            sources.append(SourceItem(
                url=url,
                source=chunk.get("source", ""),
                score=chunk.get("score", 0.0),
            ))
            seen.add(url)

    return AskResponse(
        question=question,
        answer=result["answer"],
        sources=sources,
        time_taken=round(time.time() - start, 2),
    )