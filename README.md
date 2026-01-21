# College-AI

An **AI-powered, college-specific assistant for IIIT Kottayam**, built using **open-source LLMs**, **RAG (Retrieval-Augmented Generation)**, and a **secure, modular architecture**.
This project aims to guide students, answer college-related queries, and act as a smart knowledge hub for IIIT Kottayam.

---

##  Project Vision

To build a **ChatGPT-like assistant**, but **strictly focused on IIIT Kottayam**, capable of:

* Answering queries about academics, campus life, rules, facilities, etc.
* Guiding juniors and peers
* Providing verified, college-specific information
* Ensuring privacy, security, and transparency

This is a **group startup-oriented project** developed by IIIT Kottayam students.

---

##  Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI** – backend API
* **LangChain** – RAG orchestration
* **FAISS (Meta)** – vector database
* **Sentence Transformers** – embeddings
* **Ollama** – local open-source LLMs (e.g., Mistral)
* **uv** – modern Python dependency & venv manager

### Frontend (planned)

* React / Next.js (or similar)

### Security

* Rate limiting
* Environment-based secrets
* Secure API design

---

##  High-Level Architecture

```
User → Frontend → FastAPI Backend
                     │
                     ├── LLM (Ollama)
                     ├── FAISS Vector Store
                     └── College Knowledge Base (PDFs, Docs)
```

The assistant uses **RAG**:

1. User question
2. Relevant college documents retrieved from FAISS
3. Context + question sent to LLM
4. Accurate, college-specific answer returned

---

## 📂 Repository Structure

```
College_AI/
│
├── backend/                # Core AI backend
│   ├── app/                # Application source code
│   │   ├── main.py         # FastAPI entry point
│   │   ├── api/            # API routes
│   │   ├── core/           # Config, settings, startup logic
│   │   ├── rag/            # RAG pipeline (retrieval + generation)
│   │   ├── models/         # Pydantic models
│   │   └── utils/          # Helper utilities
│   │
│   ├── data/               # Raw college documents (PDFs, text)
│   ├── vectorstore/        # FAISS index storage
│   └── tests/              # Backend tests
│   
|
│
├── frontend/               # Frontend application (planned)
├── security/               # Security research & implementation
├── docs/                   # Documentation & design notes
│
├── .gitignore              # Files ignored by Git
├── pyproject.toml          # Project metadata & dependencies
├── uv.lock                 # Locked dependency versions
├── .env.example            # Environment variable template
└── README.md               # Main project README (this file)
```

---

## 🧾 Important Files Explained

### `pyproject.toml`

* Central configuration file for Python
* Defines:

  * Project metadata
  * Dependencies
  * Development tools (black, ruff, pytest)
  * Virtual environment name (`College-AI`)

### `uv.lock`

* Auto-generated lock file
* Ensures **same dependency versions** for all contributors
* Must be committed

### `.env.example`

* Template for environment variables
* Contains **no secrets**
* Each developer creates their own `.env`

### `vectorstore/`

* Stores FAISS indexes
* Enables fast semantic search over college documents

---

##  Setup Instructions (Local Development)

### 1️⃣ Clone the repository

* create a folder of with name of your choice open cmd in the folder and paste this command
```bash
git clone https://github.com/Sparrowspidey/College-Ai.git
```

---

### 2️⃣ Install uv (one-time)

```bash
pip install uv
```

---

### 3️⃣ Create & sync virtual environment

```bash
uv sync
```

Activate the environment:

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate
```

You should see:

```
(College-AI)
```

---

### 4️⃣ Setup environment variables

```bash
cp .env.example .env
```

Edit `.env` and add required values.

---

### 5️⃣ Run the backend server

```bash
uvicorn app.main:app --reload
```

API available at:

```
http://127.0.0.1:8000
```

Docs:

```
http://127.0.0.1:8000/docs
```

---

##  Security Considerations

* No secrets committed to GitHub
* Rate limiting enabled
* Local LLMs → no external data leakage
* Designed for future authentication & role-based access

---

##  Git Workflow (Team)

* `main` → stable branch
* Feature branches → `name/feature`
* Use **Pull Requests** to merge
* Do NOT commit virtual environments

---

##  Roadmap

* [ ] Core RAG pipeline
* [ ] IIITK knowledge ingestion
* [ ] Secure API layer
* [ ] Frontend UI
* [ ] Authentication
* [ ] Deployment

---

##  Contributors

1. Vivek Ediga alias Sparrowpsidey
2. Himasai Vihar
3. Hiranya Venkata Reddy
4. Vinay V
5. Sai Akilesh 
6. Adithya M
7. Joyal Kumar J
8. Praising Harris


---

##  License

MIT License

---

> **College-AI** — Built by students, for students of IIIT Kottayam.
