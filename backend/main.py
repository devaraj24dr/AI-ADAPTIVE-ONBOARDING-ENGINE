# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : API Gateway
#  Description : FastAPI backend — connects all modules
#  Team        : TENSOR TITANS
# ============================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from parser  import pull_skills
from matcher import find_gaps
from graph   import generate_path, format_roadmap
from bkt     import LearnerSession


# ---------- App Setup ----------

engine = FastAPI(
    title       = "TENSOR TITANS — Onboarding Engine",
    description = "AI-powered adaptive learning path generator",
    version     = "1.0.0"
)

engine.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)

# Temp folder for uploaded files
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory learner sessions
active_sessions = {}


# ---------- Routes ----------

@engine.get("/")
def health_check():
    return {"status": "TENSOR TITANS Engine is Running!"}


@engine.post("/analyze")
async def analyze_profile(
    resume : UploadFile = File(...),
    jd     : UploadFile = File(...)
):
    """
    Upload resume + job description PDFs.
    Returns skill gaps + personalized learning roadmap.
    """

    # Save uploaded files temporarily
    resume_ext = os.path.splitext(resume.filename)[1].lower()
    jd_ext     = os.path.splitext(jd.filename)[1].lower()

    resume_path = f"{UPLOAD_DIR}/resume{resume_ext}"
    jd_path     = f"{UPLOAD_DIR}/jd{jd_ext}"

    with open(resume_path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd.file, f)

    # Step 1 — Extract skills
    candidate_skills = pull_skills(resume_path, mode="resume")
    required_skills  = pull_skills(jd_path,     mode="jd")

    # Step 2 — Find gaps
    gap_result = find_gaps(candidate_skills, required_skills)

    # Step 3 — Generate roadmap
    raw_path  = generate_path(gap_result["gaps"], candidate_skills)
    roadmap   = format_roadmap(raw_path)

    return {
        "candidate_skills" : candidate_skills,
        "required_skills"  : required_skills,
        "matched"          : gap_result["matched"],
        "gaps"             : gap_result["gaps"],
        "readiness_score"  : gap_result["score"],
        "roadmap"          : roadmap
    }


@engine.post("/quiz/{learner_name}")
def submit_quiz(
    learner_name : str,
    skill        : str,
    correct      : bool
):
    """
    Submit a quiz result for a learner.
    Updates mastery tracking in real time.
    """
    if learner_name not in active_sessions:
        active_sessions[learner_name] = LearnerSession(learner_name)

    session = active_sessions[learner_name]
    mastery = session.record(skill, correct)

    return {
        "learner"     : learner_name,
        "skill"       : skill,
        "mastery"     : mastery,
        "mastered"    : mastery >= 0.80,
        "weak_skills" : session.get_weak_skills()
    }


@engine.get("/report/{learner_name}")
def get_report(learner_name: str):
    """Get full progress report for a learner."""
    if learner_name not in active_sessions:
        return {"error": "Learner not found"}

    return active_sessions[learner_name].full_report()