import os
import json
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

# 🔐 Secure key loading
key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

# Configure model safely
if key:
    genai.configure(api_key=key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
else:
    model = None


# 🎯 Question Bank
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


# 🧠 Generate Questions
def generate_questions(tech):
    skills = [x.strip().lower() for x in tech.split(",")]
    qs = []

    for skill in skills:
        if skill in BANK:
            qs.extend(random.sample(BANK[skill], min(2, len(BANK[skill]))))
        else:
            qs.append(f"Explain your experience with {skill}.")

    return qs[:5]


# 🟡 Local fallback evaluator (ALWAYS WORKS)
def local_evaluate(question, answer):
    keywords = {
        "primary key": ["unique", "not null", "identifier"],
        "join": ["combine", "tables", "rows", "condition"],
        "oop": ["class", "object", "inheritance", "polymorphism"],
    }

    score = 0
    answer_lower = answer.lower()

    for key, words in keywords.items():
        if key in question.lower():
            for word in words:
                if word in answer_lower:
                    score += 2

    score = min(score, 10)

    return {
        "score": score if score > 0 else 5,
        "feedback": "Basic evaluation applied based on keywords.",
        "result": "Fallback"
    }


# ⚡ Cache to reduce API calls
@st.cache_data
def cached_ai_eval(question, answer):
    prompt = f"""
You are a technical interviewer.

Evaluate the candidate answer.

Question: {question}
Candidate Answer: {answer}

Rules:
- Score out of 10
- Be strict but fair
- Return ONLY JSON

Example:
{{
  "score": 8,
  "feedback": "Good understanding.",
  "result": "Correct"
}}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == 0:
        raise Exception("Invalid JSON")

    data = json.loads(text[start:end])

    return {
        "score": int(data.get("score", 6)),
        "feedback": data.get("feedback", "Evaluated."),
        "result": data.get("result", "Partial")
    }


# 🧠 Main evaluation function
def evaluate_answer(question, answer, index=0):

    # ❌ Empty answer
    if answer.strip() == "":
        return {
            "score": 0,
            "feedback": "No answer submitted.",
            "result": "Unanswered"
        }

    # 🔥 LIMIT API USAGE (only first 2 questions use AI)
    if index < 2 and model:
        try:
            return cached_ai_eval(question, answer)

        except Exception as e:
            error_text = str(e).lower()

            # 🚨 Handle API issues cleanly
            if "quota" in error_text or "rate" in error_text:
                return local_evaluate(question, answer)

            if "api key" in error_text or "403" in error_text:
                return local_evaluate(question, answer)

            return local_evaluate(question, answer)

    # 🟡 Fallback for remaining questions
    return local_evaluate(question, answer)
        
