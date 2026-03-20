# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : Learning Path Architect
#  Description : Builds skill graph & generates learning paths
#  Team        : TENSOR TITANS
# ============================================================

import networkx as nx


# ---------- Skill Dependency Map ----------

SKILL_TREE = {
    "Python Basics"      : ["OOP", "File Handling", "Error Handling"],
    "OOP"                : ["Design Patterns", "Flask", "FastAPI"],
    "Flask"              : ["REST APIs", "Authentication"],
    "FastAPI"            : ["REST APIs", "Authentication"],
    "REST APIs"          : ["Docker", "API Testing"],
    "Docker"             : ["Kubernetes", "CI/CD"],
    "SQL Basics"         : ["PostgreSQL", "Query Optimization"],
    "PostgreSQL"         : ["Database Design"],
    "Machine Learning"   : ["Deep Learning", "Model Deployment"],
    "Deep Learning"      : ["NLP", "Computer Vision"],
    "NLP"                : ["LLMs", "Text Classification"],
    "Data Analysis"      : ["Data Visualization", "Machine Learning"],
    "JavaScript Basics"  : ["React", "Node.js"],
    "React"              : ["Redux", "Next.js"],
    "Node.js"            : ["Express.js", "REST APIs"],
    "Linux Basics"       : ["Shell Scripting", "Docker"],
    "Git Basics"         : ["CI/CD", "GitHub Actions"],
}


# ---------- Graph Builder ----------

def _build_graph():
    """Constructs a directed skill dependency graph."""
    G = nx.DiGraph()
    for parent, children in SKILL_TREE.items():
        for child in children:
            G.add_edge(parent, child)
    return G


# ---------- Path Generator ----------

def generate_path(missing_skills, known_skills):
    """
    Main entry point.
    Takes missing skills + known skills,
    returns an ordered learning roadmap.
    """
    G = _build_graph()
    roadmap = []

    for target in missing_skills:
        # If target exists in graph, find best entry point
        if target in G.nodes:
            # Find all ancestor nodes needed
            ancestors = nx.ancestors(G, target)
            # Filter out already known skills
            needed = [
                node for node in ancestors
                if node not in known_skills
            ]
            # Add in topological order
            sub = G.subgraph(set(needed) | {target})
            try:
                ordered = list(nx.topological_sort(sub))
                for step in ordered:
                    if step not in roadmap and step not in known_skills:
                        roadmap.append(step)
            except nx.NetworkXUnfeasible:
                if target not in roadmap:
                    roadmap.append(target)
        else:
            # Skill not in graph — add directly
            if target not in roadmap and target not in known_skills:
                roadmap.append(target)

    print(f"[TENSOR TITANS] Roadmap generated: {len(roadmap)} steps")
    return roadmap


# ---------- Roadmap Formatter ----------

def format_roadmap(roadmap):
    """Converts raw roadmap list into structured step-by-step plan."""
    structured = []
    for idx, skill in enumerate(roadmap, start=1):
        structured.append({
            "step"  : idx,
            "skill" : skill,
            "status": "pending"
        })
    return structured