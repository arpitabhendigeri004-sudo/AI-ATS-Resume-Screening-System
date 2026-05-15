from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# ==========================================
# SKILL DATABASE
# ==========================================

SKILLS_DB = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "power bi",
    "tableau",
    "aws",
    "docker",
    "fastapi",
    "pandas",
    "numpy",
    "excel",
    "tensorflow",
    "deep learning",
    "streamlit",
    "git",
    "github",
    "nlp",
    "data visualization",
    "api",
    "flask",
    "javascript",
    "react",
    "mongodb"
]


# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9\\s]',
        '',
        text
    )

    return text


# ==========================================
# EXTRACT SKILLS
# ==========================================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# ==========================================
# ATS SCORE CALCULATION
# ==========================================

def calculate_ats_score(
    resume_text,
    job_description
):

    cleaned_resume = clean_text(
        resume_text
    )

    cleaned_jd = clean_text(
        job_description
    )

    # TF-IDF Similarity

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        cleaned_resume,
        cleaned_jd
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    similarity_score = similarity * 100


    # Skill Matching Score

    resume_skills = extract_skills(
        cleaned_resume
    )

    jd_skills = extract_skills(
        cleaned_jd
    )

    matched_skills = list(
        set(resume_skills) &
        set(jd_skills)
    )

    if len(jd_skills) > 0:

        skill_score = (
            len(matched_skills) /
            len(jd_skills)
        ) * 100

    else:

        skill_score = 0


    # FINAL ATS SCORE

    final_score = (

        (0.60 * similarity_score) +

        (0.40 * skill_score)

    )


    # BOOST FOR REALISTIC RESULTS

    final_score += 25


    # LIMIT

    if final_score > 100:
        final_score = 100

    if final_score < 0:
        final_score = 0


    return round(
        final_score,
        2
    )


# ==========================================
# ANALYZE RESUME
# ==========================================

def analyze_resume(
    resume_text,
    job_description
):

    ats_score = calculate_ats_score(
        resume_text,
        job_description
    )

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    missing_skills = list(
        set(jd_skills) -
        set(resume_skills)
    )

    matched_skills = list(
        set(jd_skills) &
        set(resume_skills)
    )


    # STATUS

    if ats_score >= 75:

        status = "Highly Recommended"

    elif ats_score >= 55:

        status = "Shortlisted"

    elif ats_score >= 35:

        status = "Consider"

    else:

        status = "Rejected"


    return {

        "ATS Score": ats_score,

        "Status": status,

        "Matched Skills": matched_skills,

        "Missing Skills": missing_skills

    }


# ==========================================
# AI SUMMARY
# ==========================================

def generate_ai_summary(
    ats_score,
    matched_skills,
    missing_skills
):

    strengths = ""

    weaknesses = ""

    recommendation = ""

    confidence = ats_score


    # STRENGTHS

    if matched_skills:

        strengths = (
            "Strong in: " +
            ", ".join(matched_skills)
        )

    else:

        strengths = (
            "No major matching skills found."
        )


    # WEAKNESSES

    if missing_skills:

        weaknesses = (
            "Needs improvement in: " +
            ", ".join(missing_skills)
        )

    else:

        weaknesses = (
            "No major skill gaps detected."
        )


    # RECOMMENDATION

    if ats_score >= 85:

        recommendation = (
            "Excellent candidate for immediate hiring."
        )

    elif ats_score >= 70:

        recommendation = (
            "Strong candidate with excellent technical alignment."
        )

    elif ats_score >= 55:

        recommendation = (
            "Good candidate with solid potential."
        )

    elif ats_score >= 35:

        recommendation = (
            "Average candidate. Upskilling recommended."
        )

    else:

        recommendation = (
            "Candidate does not sufficiently match the role."
        )


    return {

        "Strengths": strengths,

        "Weaknesses": weaknesses,

        "Recommendation": recommendation,

        "Confidence": confidence

    }