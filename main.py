from src.cleaner import clean_text
from src.skills import extract_skills
from src.ranking import rank_resumes


# =========================
# LOAD JOB DESCRIPTION
# =========================

with open("data/job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

clean_jd = clean_text(job_description)

jd_skills = extract_skills(clean_jd)


# =========================
# RANK RESUMES
# =========================

ranking_df = rank_resumes(
    "resumes",
    clean_jd,
    jd_skills
)


# =========================
# DISPLAY RESULTS
# =========================

print("\n==============================")
print(" AI ATS RESUME ANALYZER ")
print("==============================\n")

print(ranking_df)


# =========================
# SAVE CSV REPORT
# =========================

ranking_df.to_csv(
    "outputs/final_resume_report.csv",
    index=False
)

print("\nFinal ATS Report Generated!")