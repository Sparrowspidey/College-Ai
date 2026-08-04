import os
import re
import pickle


# ---------- CONFIGURATION ----------
CHUNK_SIZE  = 1200   # characters (~200 words) — enough context for RAG answers
OVERLAP     = 200    # characters (~17%) — ensures continuity across boundaries


# ---------- SMART CHUNK FUNCTION ----------
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
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
            # Walk back to the nearest word boundary (space/newline)
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


# ---------- EXTRACT URL FROM WEBSITE TXT ----------
def extract_url_and_text(raw: str) -> tuple[str, str]:
    """
    Website txt files start with 'URL: https://...'
    Extract URL as separate metadata and return clean content.
    """
    url  = ""
    lines = raw.splitlines()

    if lines and lines[0].startswith("URL:"):
        url = lines[0].replace("URL:", "").strip()
        content = "\n".join(lines[2:]).strip()   # skip URL line + blank line
    else:
        content = raw.strip()

    return url, content


# ---------- BASE DIRECTORY & PATHS ----------
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER      = os.path.join(BASE_DIR, "..", "..", "..", "data", "raw", "pdf")
TEXT_FOLDER     = os.path.join(BASE_DIR, "..", "..", "..", "data", "raw", "website")
OUTPUT_FOLDER   = os.path.join(BASE_DIR, "..", "..", "..", "data", "processed")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


chunks_with_metadata = []


# ---------- PROCESS WEBSITE TXT FILES ----------
print("\n📄 Processing website text files...")

txt_files = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]
print(f"   Found {len(txt_files)} files")

for file in txt_files:
    file_path = os.path.join(TEXT_FOLDER, file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw  = f.read()

        url, content = extract_url_and_text(raw)

        if not content.strip():
            print(f"   ⚠ Skipped (empty): {file}")
            continue

        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                chunks_with_metadata.append({
                    "text":    chunk,
                    "source":  file,
                    "url":     url,
                    "type":    "website",
                    "chunk_id": i,
                })

        print(f"   ✓ {file} → {len(chunks)} chunks")

    except Exception as e:
        print(f"   ✗ Failed: {file} → {e}")


# ---------- PROCESS PDF FILES ----------
print("\n📑 Processing PDF files...")

# Import pypdf (modern replacement for deprecated PyPDF2)
try:
    from pypdf import PdfReader
    print("   Using pypdf ✓")
except ImportError:
    try:
        from PyPDF2 import PdfReader
        print("   Using PyPDF2 (consider upgrading to pypdf)")
    except ImportError:
        print("   ✗ ERROR: Neither pypdf nor PyPDF2 installed.")
        print("          Run: pip install pypdf")
        exit(1)

pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
print(f"   Found {len(pdf_files)} files")

for file in pdf_files:
    file_path = os.path.join(PDF_FOLDER, file)
    try:
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        if not text.strip():
            print(f"   ⚠ Skipped (no extractable text — may be scanned): {file}")
            continue

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                chunks_with_metadata.append({
                    "text":    chunk,
                    "source":  file,
                    "url":     "",
                    "type":    "pdf",
                    "chunk_id": i,
                })

        print(f"   ✓ {file} → {len(chunks)} chunks")

    except Exception as e:
        print(f"   ✗ Failed: {file} → {e}")


# ---------- SAVE OUTPUT ----------
output_path = os.path.join(OUTPUT_FOLDER, "chunks_with_metadata.pkl")
with open(output_path, "wb") as f:
    pickle.dump(chunks_with_metadata, f)

print(f"\n✅ Chunking complete!")
print(f"   Total chunks : {len(chunks_with_metadata)}")
print(f"   Output saved : {output_path}")