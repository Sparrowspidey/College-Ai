

"""
Central configuration constants for College_AI.

This module defines the project root and key filesystem paths
(backend, app, data, docs, frontend, vector store, logs, and security),
along with default AI runtime settings such as embedding model,
LLM provider/model, FAISS index location, and retrieval top-k results.

These values are intended to be imported across the codebase to keep
path resolution and core defaults consistent in one place.
"""


from pathlib import Path

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[3]


BACKEND_DIR = PROJECT_ROOT / "backend"
APP_DIR = BACKEND_DIR / "app"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"
LOGS_DIR = PROJECT_ROOT / "logs"
SECURITY_DIR = PROJECT_ROOT / "security"

FAISS_INDEX_DIR = VECTORSTORE_DIR / "faiss_index"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

LLM_PROVIDER = "ollama"
LLM_MODEL_NAME = "Mistral"

TOP_K_RESULTS = 5

