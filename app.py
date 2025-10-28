import streamlit as st
from keyword_extraction import extract_keywords
from resume_analyzer import extract_resume_text
from ats import calculate_ats_score
from comparison import find_missing_keywords
from chat_coach import coach_reply


def main():
    st.set_page_config(page_title="AI Resume Builder", layout="wide")

   # Read and inject CSS from styles.css
    with open("styes.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Title with custom CSS class
    st.markdown('<h1 class="title">Resume Analyzer</h1>', unsafe_allow_html=True)

    # Initialize session state
    if 'job_desc_text' not in st.session_state:
        st.session_state.job_desc_text = ""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'job_keywords' not in st.session_state:
        st.session_state.job_keywords = []
    if 'resume_texts' not in st.session_state:
        st.session_state.resume_texts = []
    if 'missing_keywords' not in st.session_state:
        st.session_state.missing_keywords = []
    if 'ats_scores' not in st.session_state:
        st.session_state.ats_scores = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # [{"role":"user"/"assistant","content": "..."}]
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    if 'last_resume_text' not in st.session_state:
        st.session_state.last_resume_text = ""


    # Sidebar for inputs

    st.session_state.job_desc_text = st.sidebar.text_area("Enter the job description:", st.session_state.job_desc_text)
    if st.sidebar.button("Clear"):
        st.session_state.job_desc_text=""

    st.session_state.uploaded_files = st.sidebar.file_uploader("Upload your resume files (PDF):", type="pdf", accept_multiple_files=True)

    if st.sidebar.button("Analyze"):
        if st.session_state.uploaded_files and st.session_state.job_desc_text:
            with st.spinner("Analyzing..."):
                # Extract keywords from job description
                st.session_state.job_keywords = extract_keywords(st.session_state.job_desc_text)
                st.subheader("Extracted Keywords from Job Description")
                st.write(" | ".join(st.session_state.job_keywords))

                # Process each uploaded resume file
                st.session_state.resume_texts = []
                st.session_state.missing_keywords = []
                st.session_state.ats_scores = []

                for uploaded_file in st.session_state.uploaded_files:
                    resume_text = extract_resume_text(uploaded_file)
                    st.session_state.resume_texts.append(resume_text)

                    # Find missing keywords
                    missing_keywords = find_missing_keywords(st.session_state.job_keywords, resume_text)
                    st.session_state.missing_keywords.append(missing_keywords)

                    # Calculate ATS score
                    ats_score = calculate_ats_score(st.session_state.job_keywords, resume_text)
                    st.session_state.ats_scores.append(ats_score)

                # Display results for each resume
                for i, uploaded_file in enumerate(st.session_state.uploaded_files):
                    st.subheader(f"Results for {uploaded_file.name}")
                    st.write("Missing Keywords: " + " | ".join(st.session_state.missing_keywords[i]))
                    st.write(f"Resume Match Score: {st.session_state.ats_scores[i]}%")
        # Build a simple analysis object for chat from the first resume (or last processed)
            if st.session_state.resume_texts:
            # pick the first resume for the chat context; you can add a selector later
                _resume_text_for_chat = st.session_state.resume_texts[0]
                _missing_for_chat = st.session_state.missing_keywords[0] if st.session_state.missing_keywords else []
                _score_for_chat = st.session_state.ats_scores[0] if st.session_state.ats_scores else 0.0

            # Optional: coverage breakdown from your extracted keywords
                coverage_breakdown = {}
                for kw in st.session_state.job_keywords:
                    coverage_breakdown[kw] = 1.0 if kw.lower() in _resume_text_for_chat.lower() else 0.0

                st.session_state.last_analysis = {
                    "coverage_score": _score_for_chat,
                    "missing_keywords": _missing_for_chat,
                    "coverage_breakdown": coverage_breakdown,
                }
                st.session_state.last_resume_text = _resume_text_for_chat

            else:
                st.error("Please enter the job description and upload at least one resume.")

    if st.sidebar.button("Start Over"):
        st.session_state.clear()
    st.markdown("---")
    st.subheader("💬 Resume Coach (Chat)")

    if st.session_state.last_analysis is None:
        st.info("Run an analysis first (enter JD + upload at least one resume), then chat here.")
    else:
        # one-click suggestion run
        if st.button("Generate tailored suggestions"):
            reply = coach_reply(
                st.session_state.job_desc_text,
                st.session_state.last_resume_text,
                st.session_state.last_analysis,
                st.session_state.chat_history
            )
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # chat input
        user_msg = st.chat_input("Ask a follow-up (e.g., rewrite my summary, strengthen bullets for SQL/ETL)")
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            reply = coach_reply(
                st.session_state.job_desc_text,
                st.session_state.last_resume_text,
                st.session_state.last_analysis,
                st.session_state.chat_history
            )
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # render chat
        for msg in st.session_state.chat_history[-12:]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(msg["content"])


    # Footer
    st.markdown("""
    <div class="footer">
        <p>Developed by Mansi</p>
    </div>
    <style>
    .footer {
        position: fixed;
        right: 0;
        bottom: 0;
        background-color: #030303;
        text-align: right;
        padding: 10px;
        color: white;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()