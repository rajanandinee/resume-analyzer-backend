# models/resume_model.py
from pydantic import BaseModel
from typing import List

class ResumeAnalysis(BaseModel):
    ats_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    job_roles: List[str]
    salary_estimate: str
    recommendations: List[str]
    summary: str
