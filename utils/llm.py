import os
import json
import random
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# 🔐 Load environment
load_dotenv(override=True)

# 🔐 Secure API key
key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

# 🤖 Configure Groq client
if key:
    client = Groq(api_key=key)
else:
    client = None


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


# 🧠 Generate Questions
def generate_questions(tech):

    skills = [x.strip().lower() for x in tech.split(",")]

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

    # If AI unavailable
    if not client:
        return fallback_questions

    prompt = f"""
You are a technical interviewer.

Generate 5 technical interview questions based on these technologies:

{tech}

Rules:
- Beginner to intermediate level
- Practical understanding focused
- Return ONLY a Python list

Example:
[
    "Explain OOP in Python.",
    "What is JOIN in SQL?"
]
"""

    try:

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = completion.choices[0].message.content.strip()

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


# 🟡 Local fallback evaluator
def local_evaluate(question, answer):

    keywords = {
        "primary key": ["unique", "not null", "identifier"],
        "join": ["combine", "tables", "rows"],
        "oop": ["class", "object", "inheritance"],
        "react": ["component", "state", "props"]
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
        feedback = "Good technical understanding shown."

    elif score >= 5:
        feedback = "Answer contains some relevant concepts."

    elif score > 0:
        feedback = "Basic understanding detected."

    else:
        feedback = "Insufficient technical explanation."

    return {
        "score": score if score > 0 else 5,
        "feedback": feedback,
        "result": "Fallback Evaluation"
    }


# ⚡ AI evaluation with caching
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
- Give score out of 10
- Be strict but fair
- Return ONLY valid JSON

Example:
{{
    "score": 8,
    "feedback": "Good understanding.",
    "result": "Correct"
}}
"""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = completion.choices[0].message.content.strip()

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

    if answer.strip() == "":
        return {
            "score": 0,
            "feedback": "No answer submitted.",
            "result": "Unanswered"
        }

    # 🔥 Use AI only for first 2 questions
    if index < 2 and client:

        try:
            return cached_ai_eval(question, answer)

        except:
            return local_evaluate(question, answer)

    # 🟡 Fallback
    return local_evaluate(question, answer)
