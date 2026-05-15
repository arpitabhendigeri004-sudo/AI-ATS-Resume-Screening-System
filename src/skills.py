import re

# Master Skill List
SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "power bi",
    "excel",
    "tableau",
    "data analysis",
    "fastapi",
    "flask",
    "django",
    "streamlit",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "git",
    "github",
    "docker",
    "aws",
    "azure"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))