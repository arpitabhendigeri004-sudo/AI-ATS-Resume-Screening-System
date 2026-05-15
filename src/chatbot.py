def recruiter_chatbot(user_input):

    user_input = user_input.lower()

    # Greetings
    if "hello" in user_input:
        return "👋 Hello Recruiter! How can I help you today?"

    # Best candidate
    elif "best candidate" in user_input:
        return "🏆 The top candidate is the one with the highest ATS score and strongest skill match."

    # Missing skills
    elif "missing skills" in user_input:
        return "📌 Missing skills are identified by comparing resume skills with the job description."

    # ATS score
    elif "ats score" in user_input:
        return "📊 ATS score is calculated using NLP similarity between resume and job description."

    # Shortlist
    elif "shortlist" in user_input:
        return "✅ Candidates above the ATS threshold are shortlisted automatically."

    # Skills
    elif "skills" in user_input:
        return "🧠 The system extracts skills like Python, SQL, AWS, Docker, ML, and more."

    else:
        return "🤖 I can help with ATS scoring, candidate ranking, missing skills, and recruitment insights."