# Resume Analyzer
Click the link below to use the app!


https://airesumebuilder-kacv7znxwbpfuh428eek8f.streamlit.app/


# AI Resume Builder & Analyzer

An interactive **AI-powered Resume Analyzer** built with **Streamlit**, **OpenAI**, and **spaCy**.  
Upload your **resume (PDF)** and **job description (text)** — the app automatically extracts keywords, compares them, and calculates how well your resume matches the job posting.  

It also includes an integrated **chatbot assistant** that reviews your match score and provides personalized suggestions to improve your resume!

---

## 🚀 Features

**Resume Analysis**
- Upload a PDF resume and paste a job description.
- Automatically extracts relevant keywords using NLP (spaCy).
- Calculates a **keyword match score** showing how closely your resume fits the job.

**AI Chatbot Feedback**
- The built-in chatbot uses OpenAI to interpret the analysis results.
- Provides suggestions to improve your resume wording and keyword alignment.

**Visual Insights**
- Displays number of keywords matched vs. missing.
- Highlights optimization opportunities.

**Secure Environment**
- Sensitive API keys are handled via Streamlit Secrets — never stored in code.

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **NLP** | spaCy |
| **AI Assistant** | OpenAI API |
| **PDF Processing** | pdfplumber |
| **Deployment** | Streamlit Cloud |

---

## Installation (Local)

### 1️ Clone the repository
```bash
git clone https://github.com/mansisrinivas/AI_Resume_Builder.git
cd AI_Resume_Builder

