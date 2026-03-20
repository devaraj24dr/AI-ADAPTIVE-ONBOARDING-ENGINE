# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : Skill Gap Analyzer
#  Description : Compares candidate skills vs role requirements
#  Team        : TENSOR TITANS
# ============================================================

from sentence_transformers import SentenceTransformer, util

# Load once, reuse everywhere
_encoder = SentenceTransformer("all-MiniLM-L6-v2")


# ---------- Core Comparison ----------

def _similarity_score(skill_a, skill_b):
    """Returns a 0–1 similarity score between two skill strings."""
    vec_a = _encoder.encode(skill_a, convert_to_tensor=True)
    vec_b = _encoder.encode(skill_b, convert_to_tensor=True)
    return float(util.cos_sim(vec_a, vec_b))


def _is_covered(required_skill, candidate_skills, threshold=0.75):
    """
    Checks if a required skill is already covered
    by any skill in the candidate's profile.
    """
    for owned in candidate_skills:
        if _similarity_score(required_skill, owned) >= threshold:
            return True
    return False


# ---------- Gap Detection ----------

def find_gaps(candidate_skills, role_skills):
    """
    Main entry point.
    Returns a dict with:
      - gaps     : skills the candidate is missing
      - matched  : skills already covered
      - score    : readiness percentage
    """
    gaps    = []
    matched = []

    for requirement in role_skills:
        if _is_covered(requirement, candidate_skills):
            matched.append(requirement)
        else:
            gaps.append(requirement)

    total = len(role_skills)
    readiness = round((len(matched) / total) * 100, 1) if total > 0 else 0.0

    print(f"[TENSOR TITANS] Readiness Score : {readiness}%")
    print(f"[TENSOR TITANS] Matched Skills  : {len(matched)}")
    print(f"[TENSOR TITANS] Missing Skills  : {len(gaps)}")

    return {
        "gaps"     : gaps,
        "matched"  : matched,
        "score"    : readiness
    }