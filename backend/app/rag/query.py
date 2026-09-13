"""
rag/query.py
============
RAG Pipeline — Terminal Query Interface

Loads all resources and runs the full RAG pipeline
in an interactive terminal loop for testing.

Usage:
    cd backend
    python -m app.rag.query
"""

import pickle
import sys
import time

from app.config.config import FAISS_INDEX_PATH, CHUNKS_PATH
from app.vectorstore.faiss_index import load_index
from app.rag.pipeline import run_rag_pipeline


def load_resources() -> tuple:
    """Load FAISS index and chunks from disk."""
    print("\n🔄 Loading resources...")

    if not FAISS_INDEX_PATH.exists():
        print(f"❌ FAISS index not found at {FAISS_INDEX_PATH}")
        print("   Run build_index.py first.")
        sys.exit(1)

    if not CHUNKS_PATH.exists():
        print(f"❌ Chunks file not found at {CHUNKS_PATH}")
        print("   Run build_index.py first.")
        sys.exit(1)

    index = load_index()

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"   ✓ Chunks loaded ({len(chunks):,})")

    return index, chunks


def main() -> None:
    print("=" * 60)
    print("  College-AI — RAG Query Terminal")
    print("  Ask anything about IIIT Kottayam!")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    index, chunks = load_resources()
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
        start  = time.time()
        result = run_rag_pipeline(query, index, chunks)
        elapsed = time.time() - start

        print(f"\n🤖 College-AI:\n{result['answer']}")

        if result["context"]:
            print(f"\n📚 Sources ({elapsed:.1f}s):")
            seen = set()
            for chunk in result["context"]:
                src = chunk.get("url") or chunk.get("source", "")
                if src and src not in seen:
                    score = chunk.get("score", 0)
                    print(f"   • {src}  (score: {score:.3f})")
                    seen.add(src)
        print()


if __name__ == "__main__":
    main()