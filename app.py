import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

from src.resume_parser import extract_text
from src.ai_scorer import (
    analyze_resume,
    generate_ai_summary
)

from src.chatbot import recruiter_chatbot


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI ATS Dashboard",
    page_icon="🚀",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* GLOBAL */

html, body, [class*="css"] {
    background-color: #020617 !important;
    color: white !important;
    font-family: 'Segoe UI', sans-serif;
}

/* MAIN APP */

.stApp {
    background: linear-gradient(to right, #020617, #0f172a);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #020617 !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* HERO */

.hero-box {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    padding: 40px;
    border-radius: 25px;
    margin-bottom: 30px;
    box-shadow: 0 0 35px rgba(124,58,237,0.35);
}

.hero-box h1 {
    color: white !important;
    font-size: 52px;
    margin-bottom: 10px;
}

.hero-box h3 {
    color: #f1f5f9 !important;
    font-size: 24px;
}

/* SECTION TITLE */

.section-title {
    color: white !important;
    font-size: 30px;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* METRIC CARDS */

.metric-card {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 28px;
    border-radius: 24px;
    text-align: center;
    min-height: 180px;
    box-shadow: 0 0 25px rgba(0,255,255,0.12);
}

.metric-card h3 {
    color: #cbd5e1 !important;
    font-size: 20px;
    margin-bottom: 15px;
}

.metric-card h1 {
    color: white !important;
    font-size: 50px;
    margin: 0;
}

/* CARD */

.candidate-card {
    background: rgba(15,23,42,0.95);
    padding: 22px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    min-height: 620px;
    box-shadow: 0 0 18px rgba(0,255,255,0.08);
    margin-bottom: 20px;
}

.candidate-card h2,
.candidate-card h3,
.candidate-card p {
    color: white !important;
}

/* BADGE */

.rank-badge {
    background: linear-gradient(to right, #f59e0b, #ef4444);
    padding: 8px 15px;
    border-radius: 50px;
    color: white !important;
    display: inline-block;
    margin-bottom: 15px;
    font-size: 14px;
}

/* INPUT */

.stTextInput input,
.stTextArea textarea {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.9);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* TABLE */

[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
}

/* BUTTON */

.stDownloadButton button {
    background: linear-gradient(to right, #2563eb, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 12px 22px;
    font-weight: bold;
}

/* CHART BOX */

.chart-box {
    background: rgba(15,23,42,0.9);
    padding: 20px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.markdown("# AI ATS")
    st.caption("Recruitment Intelligence Platform")

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Candidates",
            "Analytics",
            "Reports"
        ],
        icons=[
            "speedometer2",
            "people",
            "bar-chart",
            "file-earmark"
        ],
        default_index=0
    )


# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero-box">
    <h1>🚀 AI ATS Resume Screening Dashboard</h1>
    <h3>Smart AI-Powered Recruitment & Candidate Intelligence</h3>
</div>
""", unsafe_allow_html=True)


# ==========================================
# JOB DESCRIPTION
# ==========================================

st.markdown(
    '<div class="section-title">📝 Job Description</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="""
Required Skills:
Python
SQL
Machine Learning
AWS
Docker
FastAPI
"""
)


# ==========================================
# FILE UPLOAD
# ==========================================

st.markdown(
    '<div class="section-title">📤 Upload Resumes</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, or TXT resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)


# ==========================================
# ANALYSIS
# ==========================================

if uploaded_files and job_description:

    uploaded_data = []

    for file in uploaded_files:

        text = extract_text(file)

        analysis = analyze_resume(
            text,
            job_description
        )

        summary = generate_ai_summary(

            analysis["ATS Score"],

            analysis["Matched Skills"],

            analysis["Missing Skills"]

        )

        uploaded_data.append({

            "Candidate": file.name,

            "ATS Score":
            analysis["ATS Score"],

            "Status":
            analysis["Status"],

            "Matched Skills":
            ", ".join(
                analysis["Matched Skills"]
            ),

            "Missing Skills":
            ", ".join(
                analysis["Missing Skills"]
            ),

            "Strengths":
            summary["Strengths"],

            "Weaknesses":
            summary["Weaknesses"],

            "Recommendation":
            summary["Recommendation"],

            "Confidence":
            summary["Confidence"]

        })

    upload_df = pd.DataFrame(uploaded_data)

    upload_df = upload_df.sort_values(
        by="ATS Score",
        ascending=False
    )

    # ==========================================
    # METRICS
    # ==========================================

    total_candidates = len(upload_df)

    shortlisted = len(
        upload_df[
            upload_df["Status"] == "Shortlisted"
        ]
    )

    rejected = len(
        upload_df[
            upload_df["Status"] == "Rejected"
        ]
    )

    avg_score = round(
        upload_df["ATS Score"].mean(),
        2
    )

    st.markdown(
        '<div class="section-title">📊 ATS Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("👥 Total Candidates", total_candidates),
        ("✅ Shortlisted", shortlisted),
        ("❌ Rejected", rejected),
        ("📈 Avg ATS Score", f"{avg_score}%")
    ]

    for col, card in zip(
        [col1, col2, col3, col4],
        cards
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <h3>{card[0]}</h3>
                <h1>{card[1]}</h1>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # ANALYTICS
    # ==========================================

    st.markdown(
        '<div class="section-title">📈 Analytics</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([2,1])

    with left:

        fig = px.bar(
            upload_df,
            x="Candidate",
            y="ATS Score",
            color="ATS Score",
            text="ATS Score",
            template="plotly"
        )

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="white",
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        pie = px.pie(
            upload_df,
            names="Status",
            hole=0.5,
            template="plotly"
        )

        pie.update_layout(
            paper_bgcolor="#0f172a",
            font_color="white",
            height=420
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    # ==========================================
    # TOP CANDIDATES
    # ==========================================

    st.markdown(
        '<div class="section-title">🏆 Top Candidates</div>',
        unsafe_allow_html=True
    )

    top_candidates = upload_df.head(3)

    cols = st.columns(3)

    for idx, (_, row) in enumerate(
        top_candidates.iterrows()
    ):

        with cols[idx]:

            st.markdown(f"""
            <div class="candidate-card">

                <div class="rank-badge">
                    Rank #{idx+1}
                </div>

                <h2>📄 {row['Candidate']}</h2>

                <h3>ATS Score: {row['ATS Score']}%</h3>

                <p><b>Status:</b> {row['Status']}</p>

                <p><b>Matched Skills:</b></p>

                <p>{row['Matched Skills']}</p>

                <p><b>Missing Skills:</b></p>

                <p>{row['Missing Skills']}</p>

                <p><b>Strengths:</b></p>

                <p>{row['Strengths']}</p>

                <p><b>Weaknesses:</b></p>

                <p>{row['Weaknesses']}</p>

                <p><b>AI Recommendation:</b></p>

                <p>{row['Recommendation']}</p>

                <p><b>Hiring Confidence:</b></p>

                <p>{row['Confidence']}%</p>

            </div>
            """, unsafe_allow_html=True)

            st.progress(
                int(row["ATS Score"])
            )

    # ==========================================
    # TABLE
    # ==========================================

    st.markdown(
        '<div class="section-title">📋 Candidate Analysis</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        upload_df,
        use_container_width=True,
        height=350
    )

    # ==========================================
    # DOWNLOAD REPORT
    # ==========================================

    csv = upload_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download ATS Report",
        data=csv,
        file_name="ATS_Report.csv",
        mime="text/csv"
    )


# ==========================================
# AI CHATBOT
# ==========================================

st.markdown(
    '<div class="section-title">🤖 AI Recruiter Assistant</div>',
    unsafe_allow_html=True
)

user_query = st.text_input(
    "Ask the AI Recruiter"
)

if user_query:

    response = recruiter_chatbot(
        user_query
    )

    st.markdown(f"""
    <div class="candidate-card">
        <h3>🤖 AI Response</h3>
        <p>{response}</p>
    </div>
    """, unsafe_allow_html=True)