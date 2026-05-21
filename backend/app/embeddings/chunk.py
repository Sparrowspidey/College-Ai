import os
import pickle
import PyPDF2

chunks_with_metadata = []

# ---------- CUSTOM CHUNK FUNCTION ----------

def chunk_text(text, chunk_size=500, overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

# ---------- BASE DIRECTORY ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- UPDATED PATHS ----------

PDF_FOLDER = os.path.join(BASE_DIR, "..", "..", "data", "raw", "pdf")

TEXT_FOLDER = os.path.join(BASE_DIR, "..", "..", "data", "raw", "website")

# ---------- PROCESS WEBSITE TXT FILES ----------

for file in os.listdir(TEXT_FOLDER):

    if file.endswith(".txt"):

        file_path = os.path.join(TEXT_FOLDER, file)

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read()

            chunks = chunk_text(text)

            for chunk in chunks:

                if chunk.strip():

                    chunks_with_metadata.append({
                        "text": chunk,
                        "source": file,
                        "type": "website"
                    })

# ---------- PROCESS PDF FILES ----------

for file in os.listdir(PDF_FOLDER):

    if file.endswith(".pdf"):

        file_path = os.path.join(PDF_FOLDER, file)

        text = ""

        with open(file_path, "rb") as f:

            reader = PyPDF2.PdfReader(f)

            for page in reader.pages:

                extracted_text = page.extract_text()

                if extracted_text:
                    text += extracted_text

        chunks = chunk_text(text)

        for chunk in chunks:

            if chunk.strip():

                chunks_with_metadata.append({
                    "text": chunk,
                    "source": file,
                    "type": "pdf"
                })

# ---------- SAVE OUTPUT ----------

output_path = os.path.join(BASE_DIR, "chunks_with_metadata.pkl")

with open(output_path, "wb") as f:

    pickle.dump(chunks_with_metadata, f)

# ---------- DONE ----------

print(f"Total chunks created: {len(chunks_with_metadata)}")

print("Chunking completed successfully")