QUESTION_PROMPT = """
Generate 5 beginner to intermediate level technical interview questions
based on the candidate's tech stack.
Return only questions in numbered format.
Tech Stack: {tech}
"""

EVAL_PROMPT = """
You are a technical interviewer.

Evaluate the candidate answer.

Return JSON only in this format:

{
  "score": number out of 10,
  "feedback": "short feedback",
  "result": "Correct / Partially Correct / Wrong"
}
"""