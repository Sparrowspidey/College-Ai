"""
config.py
=========
Central configuration for College-AI.

All paths and AI settings are defined here.
Import from this file anywhere in the project — never hardcode paths.
"""

from pathlib import Path

# ── Project root (4 levels up from backend/app/config/config.py) ──────────
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# ── Directory paths ───────────────────────────────────────────────────────
BACKEND_DIR    = PROJECT_ROOT / "backend"
APP_DIR        = BACKEND_DIR  / "app"
DATA_DIR       = PROJECT_ROOT / "data"
DOCS_DIR       = PROJECT_ROOT / "docs"
FRONTEND_DIR   = PROJECT_ROOT / "frontend"
LOGS_DIR       = PROJECT_ROOT / "logs"
SECURITY_DIR   = PROJECT_ROOT / "security"

# ── Data subdirectories ───────────────────────────────────────────────────
RAW_DIR        = DATA_DIR / "raw"
WEBSITE_DIR    = RAW_DIR  / "website"
PDF_DIR        = RAW_DIR  / "pdf"
PROCESSED_DIR  = DATA_DIR / "processed"

# ── FAISS index and chunks ────────────────────────────────────────────────
FAISS_INDEX_PATH  = PROCESSED_DIR / "faiss_index.index"
CHUNKS_PATH       = PROCESSED_DIR / "chunks_for_retrieval.pkl"
CHUNKS_RAW_PATH   = PROCESSED_DIR / "chunks_with_metadata.pkl"

# ── Embedding model ───────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ── LLM (Ollama) ──────────────────────────────────────────────────────────
LLM_PROVIDER   = "ollama"
LLM_MODEL      = "mistral"
OLLAMA_URL     = "http://localhost:11434/api/generate"
OLLAMA_TIMEOUT = 120  # seconds

# ── RAG settings ──────────────────────────────────────────────────────────
TOP_K_RESULTS        = 5
SIMILARITY_THRESHOLD = 0.30

# ── Chunking settings ─────────────────────────────────────────────────────
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200