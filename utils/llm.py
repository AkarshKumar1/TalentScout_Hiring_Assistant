import os
import json
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompts import QUESTION_PROMPT, EVAL_PROMPT

load_dotenv(override=True)

key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

genai.configure(api_key=key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

BANK = {
    "python": [
        "What is list vs tuple?",
        "Explain OOP in Python.",
        "What is lambda function?"
    ],
    "sql": [
        "What is JOIN in SQL?",
        "Difference between WHERE and HAVING?",
        "What is primary key?"
    ],
    "react": [
        "What is useState?",
        "Difference between props and state?",
        "What is JSX?"
    ],
    "machine learning": [
        "What is overfitting?",
        "What is supervised learning?",
        "What is cross validation?"
    ]
}

def generate_questions(tech):
    skills = [x.strip().lower() for x in tech.split(",")]
    qs = []

    for skill in skills:
        if skill in BANK:
            qs.extend(random.sample(BANK[skill], min(2, len(BANK[skill]))))
        else:
            qs.append(f"Explain your experience with {skill}.")

    return qs[:5]

def evaluate_answer(question, answer):
    if not model or not key:
        return {
            "score": 5,
            "feedback": "AI service unavailable. Manual review recommended.",
            "result": "Review"
        }

    prompt = f"""
You are a technical interviewer.

Evaluate the candidate answer.

Question: {question}

Candidate Answer: {answer}

Rules:
- Give fair technical score out of 10
- Be strict but reasonable
- Return ONLY pure JSON

Example:
{{
  "score": 8,
  "feedback": "Good answer with correct fundamentals.",
  "result": "Correct"
}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean response
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == 0:
            raise Exception("Invalid AI response")

        json_text = text[start:end]
        data = json.loads(json_text)

        return {
            "score": int(data.get("score", 6)),
            "feedback": data.get("feedback", "Answer evaluated."),
            "result": data.get("result", "Partial")
        }

    except Exception as e:

        error_text = str(e).lower()

        # 🔥 HANDLE API KEY / NETWORK ERRORS CLEANLY
        if "api key" in error_text or "403" in error_text or "quota" in error_text:
            return {
                "score": 5,
                "feedback": "AI evaluation temporarily unavailable. Manual review recommended.",
                "result": "Unavailable"
            }

        # Generic fallback
        return {
            "score": 6,
            "feedback": "Answer received. Evaluation completed with fallback logic.",
            "result": "Partial"
        }
        }
