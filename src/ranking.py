import os
import pandas as pd

from src.ingest import extract_resume_text
from src.cleaner import clean_text
from src.skills import extract_skills
from src.matcher import calculate_similarity


def rank_resumes(resume_folder, job_description, jd_skills):

    results = []

    for file_name in os.listdir(resume_folder):

        file_path = os.path.join(resume_folder, file_name)

        # Extract Resume
        raw_text = extract_resume_text(file_path)

        # Clean Resume
        cleaned_text = clean_text(raw_text)

        # Extract Skills
        resume_skills = extract_skills(cleaned_text)

        # ATS Score
        ats_score = calculate_similarity(
            cleaned_text,
            job_description
        )

        # Matched Skills
        matched_skills = list(
            set(resume_skills) & set(jd_skills)
        )

        # Missing Skills
        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        # Shortlist Logic
        status = "Shortlisted" if ats_score >= 60 else "Rejected"

        # AI Suggestions
        suggestions = []

        if "aws" not in resume_skills:
            suggestions.append("Add cloud project experience")

        if "docker" not in resume_skills:
            suggestions.append("Learn Docker basics")

        if "machine learning" not in resume_skills:
            suggestions.append("Include ML projects")

        if len(suggestions) == 0:
            suggestions.append("Strong profile")

        # Store Results
        results.append({
            "Candidate": file_name,
            "ATS Score": ats_score,
            "Status": status,
            "Matched Skills": ", ".join(matched_skills),
            "Missing Skills": ", ".join(missing_skills),
            "Suggestions": ", ".join(suggestions)
        })

    # DataFrame
    df = pd.DataFrame(results)

    # Sort
    df = df.sort_values(
        by="ATS Score",
        ascending=False
    )

    return df