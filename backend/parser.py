# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : Document Intelligence Core
#  Description : Extracts skill signals from Resume & JD
#                Supports PDF and DOCX formats
#  Team        : TENSOR TITANS
# ============================================================

import ollama
import pdfplumber
import json
import docx
import os


# ---------- File Reader ----------

def load_document(filepath):
    """Reads text from PDF or DOCX automatically."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return _read_pdf(filepath)
    elif ext == ".docx":
        return _read_docx(filepath)
    else:
        print(f"[TENSOR TITANS] Unsupported file: {ext}")
        return ""


def _read_pdf(filepath):
    """Extracts text from PDF file."""
    collected = []
    with pdfplumber.open(filepath) as doc:
        for pg in doc.pages:
            content = pg.extract_text()
            if content:
                collected.append(content.strip())
    return "\n".join(collected)


def _read_docx(filepath):
    """Extracts text from DOCX file."""
    doc = docx.Document(filepath)
    collected = []
    for para in doc.paragraphs:
        if para.text.strip():
            collected.append(para.text.strip())
    return "\n".join(collected)


# ---------- Skill Extraction ----------

def _build_prompt(content, mode):
    """Builds LLM instruction based on document type."""
    focus = "resume of a candidate" if mode == "resume" else "job description"
    return f"""
You are a skill extraction engine analyzing a {focus}.
Your task: identify every technical and professional skill mentioned.

Rules:
- Return ONLY valid JSON
- No explanation, no extra text
- Format strictly as: {{"skills": ["skill1", "skill2"]}}

Document:
{content[:3000]}
"""


def pull_skills(filepath, mode="resume"):
    """
    Main entry point.
    Supports both PDF and DOCX files.
    mode = 'resume' → candidate skills
    mode = 'jd'     → required skills
    """
    raw_text = load_document(filepath)

    if not raw_text:
        print(f"[TENSOR TITANS] Warning: No text found in {filepath}")
        return []

    instruction = _build_prompt(raw_text, mode)

    llm_response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": instruction}]
    )

    output = llm_response["message"]["content"]

    try:
        start  = output.index("{")
        end    = output.rindex("}") + 1
        parsed = json.loads(output[start:end])
        skills = parsed.get("skills", [])
        print(f"[TENSOR TITANS] Extracted {len(skills)} skills from {mode}")
        return skills

    except (ValueError, json.JSONDecodeError) as err:
        print(f"[TENSOR TITANS] Parse error: {err}")
        return []