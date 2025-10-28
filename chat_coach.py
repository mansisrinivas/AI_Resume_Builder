# chat_coach.py
import os, json
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()  # reads .env if present

try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _client = None

SYSTEM_PROMPT = (
    "You are an ATS-aware resume coach. Given a job description, a resume, and a precomputed analysis, "
    "produce actionable improvements. Be specific, preserve truthfulness, and propose quantified bullet rewrites."
)

def coach_reply(job_desc: str, resume_text: str, analysis: Dict, chat_history: List[Dict]) -> str:
    """
    analysis example:
    {
      "coverage_score": 72.5,
      "missing_keywords": ["redshift", "airflow"],
      "coverage_breakdown": {"python": 1, "sql": 1, "etl": 1, "airflow": 0, ...}
    }
    chat_history: recent messages [{"role":"user"/"assistant","content":"..."}]
    """
    if not _client or not os.getenv("OPENAI_API_KEY"):
        return ("[Chat is disabled: set OPENAI_API_KEY in your environment or a .env file]")

    payload = {
        "job_description": job_desc.strip(),
        "resume": resume_text.strip(),
        "analysis": analysis,
        "instructions": [
            "List high-priority missing skills to add (without fabricating experience).",
            "Suggest 3 stronger bullet rewrites with metrics.",
            "Flag vague phrases and propose crisp alternatives.",
            "Offer a tailored 2–3 line summary if helpful."
        ],
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history[-6:] + [
        {
            "role": "user",
            "content": "Use this JSON to give targeted improvements:\n\n" + json.dumps(payload, ensure_ascii=False)
        }
    ]

    resp = _client.chat.completions.create(
        model="gpt-4o-mini",     # swap if needed based on your account
        messages=messages,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
