import os
import json
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv(override=True)

# 🔐 Secure API key loading
key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

# 🤖 Configure Gemini model safely
if key:
    genai.configure(api_key=key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
else:
    model = None


# 🎯 Fallback Question Bank
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


# 🧠 Dynamic AI Question Generation
def generate_questions(tech):

    skills = [x.strip().lower() for x in tech.split(",")]

    # 🔥 Fallback questions
    fallback_questions = []

    for skill in skills:
        if skill in BANK:
            fallback_questions.extend(
                random.sample(BANK[skill], min(2, len(BANK[skill])))
            )
        else:
            fallback_questions.append(
                f"Explain your experience with {skill}."
            )

    fallback_questions = fallback_questions[:5]

    # ❌ If AI unavailable
    if not model:
        return fallback_questions

    prompt = f"""
You are a technical interviewer.

Generate 5 technical interview questions based on these technologies:

{tech}

Rules:
- Questions should be beginner to intermediate level
- Focus on practical understanding
- Questions should be concise
- Return ONLY a Python list

Example:
[
    "What is JOIN in SQL?",
    "Explain OOP in Python."
]
"""

    try:
        response = model.generate_content(prompt)

        text = response.text.strip()

        # Clean markdown formatting
        text = text.replace("```python", "")
        text = text.replace("```", "").strip()

        start = text.find("[")
        end = text.rfind("]") + 1

        if start == -1 or end == 0:
            return fallback_questions

        questions = eval(text[start:end])

        if not isinstance(questions, list):
            return fallback_questions

        return questions[:5]

    except:
        return fallback_questions


# 🟡 Local Fallback Evaluator
def local_evaluate(question, answer):

    keywords = {
        "primary key": ["unique", "not null", "identifier"],
        "join": ["combine", "tables", "rows", "condition"],
        "where and having": ["where", "having", "group by"],
        "oop": ["class", "object", "inheritance", "polymorphism"],
        "react": ["component", "state", "props"],
        "machine learning": ["model", "training", "data"]
    }

    score = 0

    answer_lower = answer.lower()

    for key_text, words in keywords.items():

        if key_text in question.lower():

            for word in words:

                if word in answer_lower:
                    score += 2

    score = min(score, 10)

    if score >= 8:
        feedback = "Good technical understanding shown in the answer."

    elif score >= 5:
        feedback = "The answer includes some relevant concepts but lacks detailed explanation."

    elif score > 0:
        feedback = "Basic understanding detected, but the answer is incomplete."

    else:
        feedback = "The answer does not contain enough relevant technical concepts."

    return {
        "score": score if score > 0 else 5,
        "feedback": feedback,
        "result": "Fallback Evaluation"
    }


# ⚡ Cache AI evaluation to reduce API usage
@st.cache_data
def cached_ai_eval(question, answer):

    prompt = f"""
You are a technical interviewer.

Evaluate the candidate answer.

Question:
{question}

Candidate Answer:
{answer}

Rules:
- Give a score out of 10
- Be strict but fair
- Give concise technical feedback
- Return ONLY valid JSON

Example:
{{
    "score": 8,
    "feedback": "Good understanding of SQL joins.",
    "result": "Correct"
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Clean markdown formatting
    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == 0:
        raise Exception("Invalid JSON")

    json_text = text[start:end]

    data = json.loads(json_text)

    return {
        "score": int(data.get("score", 6)),
        "feedback": data.get("feedback", "Answer evaluated."),
        "result": data.get("result", "Partial")
    }


# 🧠 Main Evaluation Function
def evaluate_answer(question, answer, index=0):

    # ❌ Empty Answer
    if answer.strip() == "":

        return {
            "score": 0,
            "feedback": "No answer submitted.",
            "result": "Unanswered"
        }

    # 🔥 Use AI only for first 2 questions
    if index < 2 and model:

        try:
            return cached_ai_eval(question, answer)

        except Exception as e:

            error_text = str(e).lower()

            # 🚨 Handle quota / API errors safely
            if (
                "quota" in error_text
                or "rate" in error_text
                or "api key" in error_text
                or "403" in error_text
            ):

                return local_evaluate(question, answer)

            # Generic fallback
            return local_evaluate(question, answer)

    # 🟡 Local fallback for remaining questions
    return local_evaluate(question, answer)
        
