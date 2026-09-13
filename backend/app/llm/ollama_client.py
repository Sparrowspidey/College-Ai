"""
ollama_client.py
================
LLM Module — Ollama Client

Handles all communication with the locally running Ollama server.
Builds the RAG prompt and returns Mistral's generated answer.
"""

import requests
from fastapi import HTTPException

from app.config.config import OLLAMA_URL, LLM_MODEL, OLLAMA_TIMEOUT


# ── Prompt builder ────────────────────────────────────────────────────────
def build_prompt(question: str, context_chunks: list[dict]) -> str:
    """
    Build a context-grounded prompt for the LLM.

    Instructs Mistral to answer ONLY from the provided context
    and never hallucinate or guess.

    Args:
        question:       The student's question.
        context_chunks: List of chunk dicts from the vector store.

    Returns:
        Formatted prompt string.
    """
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        source = chunk.get("url") or chunk.get("source", "")
        context_parts.append(f"[{i}] {chunk['text']}\nSource: {source}")

    context = "\n\n".join(context_parts)

    return f"""You are College-AI, a helpful assistant for students of IIIT Kottayam.
Answer the question using ONLY the context provided below.
If the context does not contain enough information to answer, say so clearly.
Do not make up or guess any information.
Keep your answer clear, accurate, and student-friendly.

Context:
{context}

Question: {question}

Answer:"""


# ── LLM call ──────────────────────────────────────────────────────────────
def generate_answer(question: str, context_chunks: list[dict]) -> str:
    """
    Send prompt to Ollama and return the generated answer.

    Args:
        question:       The student's question.
        context_chunks: Retrieved chunk dicts from vector store.

    Returns:
        Answer string from Mistral.

    Raises:
        HTTPException 503 if Ollama is not running.
        HTTPException 504 if Ollama times out.
        HTTPException 502 if Ollama returns an unexpected error.
    """
    if not context_chunks:
        return (
            "I couldn't find relevant information about that "
            "in the IIIT Kottayam knowledge base."
        )

    prompt = build_prompt(question, context_chunks)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model":  LLM_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=OLLAMA_TIMEOUT,
        )

        if response.status_code == 200:
            return response.json().get("response", "No response received.").strip()

        raise HTTPException(
            status_code=502,
            detail=f"Ollama returned HTTP {response.status_code}",
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Run 'ollama serve' first.",
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama timed out. Try again.",
        )


# ── Health check ──────────────────────────────────────────────────────────
def check_ollama_health() -> bool:
    """
    Returns True if Ollama is reachable, False otherwise.
    Used by the /health endpoint.
    """
    try:
        r = requests.get("http://localhost:11434", timeout=3)
        return r.status_code == 200
    except Exception:
        return False