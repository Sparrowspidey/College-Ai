"""
chunk.py
========
Data Ingestion — Chunking Module

Reads all crawled website .txt files and downloaded PDFs,
splits them into overlapping text chunks, and saves the result
as a pickle file ready for embedding.

Usage:
    cd backend/app/ingestion/chunker
    python chunk.py

    cd backend
    python -m app.ingestion.chunker.chunk
"""

import os
import pickle
import re
import sys

# Allow imports from project root
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[4]))

from app.config.config import (
    WEBSITE_DIR, PDF_DIR, PROCESSED_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP, CHUNKS_RAW_PATH
)


# ── Smart word-boundary chunker ───────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks that respect word boundaries.
    Never cuts in the middle of a word.
    """
    chunks = []
    start  = 0
    text   = text.strip()

    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary == -1:
                boundary = text.rfind("\n", start, end)
            if boundary != -1:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ── Extract URL from website txt files ───────────────────────────────────
def extract_url_and_text(raw: str) -> tuple[str, str]:
    """
    Website txt files start with 'URL: https://...'
    Extract URL as metadata and return clean content.
    """
    lines = raw.splitlines()
    if lines and lines[0].startswith("URL:"):
        url     = lines[0].replace("URL:", "").strip()
        content = "\n".join(lines[2:]).strip()
    else:
        url     = ""
        content = raw.strip()
    return url, content


# ── Main ──────────────────────────────────────────────────────────────────
def run_chunking() -> list[dict]:
    chunks_with_metadata = []
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # ── Website txt files ─────────────────────────────────────────────────
    print("\n📄 Processing website text files...")
    txt_files = list(WEBSITE_DIR.glob("*.txt"))
    print(f"   Found {len(txt_files)} files")

    for file_path in txt_files:
        try:
            raw         = file_path.read_text(encoding="utf-8")
            url, content = extract_url_and_text(raw)

            if not content.strip():
                print(f"   ⚠ Skipped (empty): {file_path.name}")
                continue

            chunks = chunk_text(content)
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    chunks_with_metadata.append({
                        "text":     chunk,
                        "source":   file_path.name,
                        "url":      url,
                        "type":     "website",
                        "chunk_id": i,
                    })

            print(f"   ✓ {file_path.name} → {len(chunks)} chunks")

        except Exception as e:
            print(f"   ✗ Failed: {file_path.name} → {e}")

    # ── PDF files ─────────────────────────────────────────────────────────
    print("\n📑 Processing PDF files...")

    try:
        from pypdf import PdfReader
        print("   Using pypdf ✓")
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            print("   Using PyPDF2 (consider upgrading: pip install pypdf)")
        except ImportError:
            print("   ✗ ERROR: Install pypdf → pip install pypdf")
            return chunks_with_metadata

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print(f"   Found {len(pdf_files)} files")

    for file_path in pdf_files:
        try:
            text = ""
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

            if not text.strip():
                print(f"   ⚠ Skipped (scanned/image PDF): {file_path.name}")
                continue

            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    chunks_with_metadata.append({
                        "text":     chunk,
                        "source":   file_path.name,
                        "url":      "",
                        "type":     "pdf",
                        "chunk_id": i,
                    })

            print(f"   ✓ {file_path.name} → {len(chunks)} chunks")

        except Exception as e:
            print(f"   ✗ Failed: {file_path.name} → {e}")

    # ── Save ──────────────────────────────────────────────────────────────
    with open(CHUNKS_RAW_PATH, "wb") as f:
        pickle.dump(chunks_with_metadata, f)

    print(f"\n✅ Chunking complete!")
    print(f"   Total chunks : {len(chunks_with_metadata):,}")
    print(f"   Output saved : {CHUNKS_RAW_PATH}")

    return chunks_with_metadata


if __name__ == "__main__":
    run_chunking()