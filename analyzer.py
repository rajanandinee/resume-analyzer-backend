from typing import Dict
import re
from models.resume_model import ResumeAnalysis

# Define expected/ideal skills
IDEAL_SKILLS = {"python", "sql", "machine learning", "fastapi", "react", "dsa", "nlp", "docker", "git"}

JOB_ROLE_MAP = {
    "SDE-I (Software Development Engineer - I)": {"python", "dsa", "sql", "git"},
    "SDE-II (Software Development Engineer - II)": {"python", "dsa", "sql", "git", "fastapi", "docker"},
    "Data Scientist": {"python", "sql", "machine learning", "nlp"},
    "ML Engineer": {"python", "machine learning", "nlp", "docker"},
    "Backend Developer": {"python", "fastapi", "sql", "docker", "git"},
    "Frontend Developer": {"react", "git"},
    "Full Stack Developer": {"react", "fastapi", "docker", "sql", "git"},
    "DevOps Engineer": {"docker", "git", "python"},
    "DSA Specialist": {"dsa", "python"},
    "AI/ML Researcher": {"python", "machine learning", "nlp", "sql"},
}


# Salary estimator function
def estimated_salary(matched_count: int) -> str:
    if matched_count >= 8:
        return "Rs18–25 LPA"
    elif matched_count >= 6:
        return "Rs12–18 LPA"
    elif matched_count >= 4:
        return "Rs8–12 LPA"
    elif matched_count >= 2:
        return "Rs5–8 LPA"
    else:
        return "Rs3–5 LPA"

def recommend_jobs(found_skills: set):
    recommended_roles = []
    for role, required_skills in JOB_ROLE_MAP.items():
        if found_skills & required_skills:  # If any match
            recommended_roles.append(role)
    return recommended_roles if recommended_roles else ["No strong matches found"]


def analyze_resume(resume_text: str, target_role: str):
    role_skills = JOB_ROLE_MAP.get(target_role, set())
    found_skills = {skill for skill in role_skills if skill in resume_text.lower()}
    score = int((len(found_skills) / len(role_skills)) * 100) if role_skills else 0

    
    missing_skills = list(role_skills - found_skills)

    job_recommendations = recommend_jobs(found_skills)
    salary = estimated_salary(len(found_skills))
    
    suggestions = []
    if score < 50:
        suggestions.append("Consider adding more relevant skills like FastAPI, Docker, or Git.")
    if 'project' not in resume_text.lower():
        suggestions.append("Add detailed project descriptions with technologies used.")
    
    return {
        "ats_score": score,
        "matched_skills": list(found_skills),
        "suggested_skills": missing_skills,
        # "suggested_skills": suggestions,
        "job_recommendations": job_recommendations,  # Placeholder
        "estimated_salary": salary,
        "resume_text_snippet": resume_text[:10000]
    }
__all__ = ["analyze_resume", "JOB_ROLE_MAP"]
