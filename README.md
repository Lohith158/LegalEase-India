# ⚖️ LegalEase India

A production-grade AI-powered legal research assistant for Indian law queries.

🔗 **Live Demo:** https://huggingface.co/spaces/Lohi158/LegalEase-India

---

## What it does

LegalEase India lets you ask questions about Indian law and get grounded, cited answers — no hallucination, no guessing. It uses Retrieval-Augmented Generation (RAG) to search through real legal documents before answering.

- Ask questions about Indian Penal Code, RTI Act, Consumer Protection Act
- Upload your own legal PDFs and query them instantly
- Add any legal webpage URL to the knowledge base
- Every answer is grounded in source documents with citations

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | HuggingFace (paraphrase-MiniLM-L3-v2) |
| Vector DB | ChromaDB |
| RAG Framework | LangChain |
| Frontend | React (CDN, no build step) |
| Deployment | Hugging Face Spaces (Docker) |

---

## Architecture
```
User Question
     ↓
React UI
     ↓
FastAPI Server
     ↓
Safety Layer — blocks harmful/off-topic queries
     ↓
RAG Engine — searches ChromaDB
     ↓
Gemini LLM — generates grounded answer
     ↓
Audit Logger — saves to logs.json
     ↓
Answer + Source Citations
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/ask` | Ask a legal question |
| POST | `/upload` | Upload a legal PDF |
| POST | `/add-url` | Index a legal webpage |

Interactive docs: `/docs`

---

## Run Locally
```bash
git clone https://github.com/Lohith158/LegalEase-India.git
cd LegalEase-India
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create `.env`:
```
GEMINI_API_KEY=your_key_here
LLM_PROVIDER=gemini
```

Run:
```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000`

---

## Built by

**Lohith G** — Final year AIML student || AI Entusiast

[LinkedIn](https://www.linkedin.com/in/lohith-g-58680b2a6/) · [GitHub](https://github.com/Lohith158)