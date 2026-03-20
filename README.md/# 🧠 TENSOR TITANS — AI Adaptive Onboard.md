# 🧠 TENSOR TITANS — AI Adaptive Onboarding Engine

> Built for ARTPARK CodeForge Hackathon 2026

## 🎯 Problem Statement

Current corporate onboarding uses static "one-size-fits-all" training.
Experienced hires waste time on known concepts, while beginners get overwhelmed.

## 💡 Our Solution

An AI-driven adaptive learning engine that:
- Parses a new hire's resume and job description
- Identifies the exact skill gap
- Generates a personalized learning roadmap
- Tracks mastery progress dynamically

---

## 🏗️ Architecture
```
Resume + JD Upload
       ↓
Mistral LLM → Skill Extraction
       ↓
MiniLM Embeddings → Skill Gap Analysis
       ↓
NetworkX Graph → Learning Path Generation
       ↓
BKT Engine → Mastery Tracking
       ↓
Streamlit UI → Visual Dashboard
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Mistral (via Ollama) |
| Embeddings | all-MiniLM-L6-v2 |
| Skill Graph | NetworkX |
| Knowledge Tracing | Bayesian Knowledge Tracing (Custom) |
| Backend | FastAPI |
| Frontend | Streamlit |
| PDF/DOCX Parsing | pdfplumber, python-docx |

---

## 📁 Project Structure
```
TENSOR-TITANS/
├── backend/
│   ├── parser.py       # Resume & JD skill extraction
│   ├── matcher.py      # Skill gap analysis
│   ├── graph.py        # Learning path generation
│   ├── bkt.py          # Mastery tracking engine
│   └── main.py         # FastAPI gateway
├── frontend/
│   └── app.py          # Streamlit dashboard
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/download) installed

### Step 1 — Clone the repo
```bash
git clone https://github.com/devaraj24dr/AI-ADAPTIVE-ONBOARDING-ENGINE.git
cd AI-ADAPTIVE-ONBOARDING-ENGINE
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install streamlit fastapi uvicorn sentence-transformers networkx pdfplumber ollama python-multipart python-docx plotly
```

### Step 4 — Pull Mistral model
```bash
ollama pull mistral
```

### Step 5 — Run the application

**Terminal 1 — Ollama:**
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
cd backend
uvicorn main:engine --reload
```

**Terminal 3 — Frontend:**
```bash
cd frontend
streamlit run app.py
```

Open browser at: **http://localhost:8501**

---

## 🔍 How It Works

### 1. Skill Extraction
Mistral LLM reads the resume and job description, extracting all technical and professional skills as structured JSON.

### 2. Skill Gap Analysis
MiniLM embeddings convert skills into vectors. Cosine similarity (threshold: 0.75) determines if a candidate skill covers a required skill — handling synonyms like "ML" vs "Machine Learning".

### 3. Adaptive Pathing
NetworkX builds a directed skill dependency graph. The engine finds the shortest path from the candidate's current skills to the target role requirements.

### 4. Knowledge Tracing
Custom Bayesian Knowledge Tracing (BKT) tracks mastery per skill using quiz results, dynamically adjusting the learning path based on performance.

---

## 📊 Datasets Used

- [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset/data)
- [O*NET Skills Database](https://www.onetcenter.org/db_releases.html)
- [Jobs & Job Description Dataset](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description)

---

## 📈 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Readiness Score | % of required skills already matched |
| Skill Gap Count | Number of missing skills identified |
| Roadmap Steps | Ordered learning path length |
| Mastery Level | BKT probability per skill (0-1) |

---

## 👥 Team

**TENSOR TITANS**
- Built with ❤️ for ARTPARK CodeForge Hackathon 2026