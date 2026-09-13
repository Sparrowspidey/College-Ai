# College-AI

An **AI-powered, college-specific assistant for IIIT Kottayam**, built using **open-source LLMs**, **RAG (Retrieval-Augmented Generation)**, and a **secure, modular architecture**.
This project aims to guide students, answer college-related queries, and act as a smart knowledge hub for IIIT Kottayam.

---

## Document
https://docs.google.com/document/d/1u9MQ6vgbJ8CKvJ7c_ZmI0_UOqxBnH-5hp_8VKsdnaow/edit?usp=sharing

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

##  Repository Structure

```
College-AI
│
├── backend
│   └── app
│       ├── api
│       ├── rag
│       ├── vectorstore
│       ├── ingestion
│       ├── embeddings
│       └── config
│           └── settings.py
│
├── data
│   ├── documents
│   │   
│   │
│   ├── syllabus
│   │
│   └── notices
│
├── vectorstore_data
│   └── index.faiss
│
├── docs
└── README.md
```

---

##  Important Files Explained

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
1. Dr. Dhakshayani J ( Project Supervisor )
2. Vivek Ediga @ Sparrowpsidey
3. Reshmitha G
4. Himasai Vihar
5. Vinay V @DevonKaratt
6. Sai Akilesh 
7. Adithya M




---

##  License

MIT License

---

> **College-AI** — Built by students, for students of IIIT Kottayam.
