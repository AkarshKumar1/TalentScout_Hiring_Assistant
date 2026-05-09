import streamlit as st
from utils.validators import validate_email, validate_phone
from utils.storage import save_candidate
from utils.llm import generate_questions, evaluate_answer

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="TalentScout AI Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TalentScout AI Hiring Assistant")
st.caption(
    "Conversational AI-powered hiring assistant for initial candidate screening."
)

# --------------------------------
# SESSION STATE
# --------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "form"

if "candidate" not in st.session_state:
    st.session_state.candidate = {}

if "questions" not in st.session_state:
    st.session_state.questions = []

# --------------------------------
# STAGE 1 : PROFILE FORM
# --------------------------------
if st.session_state.stage == "form":

    st.subheader("📄 Candidate Information")

    with st.form("candidate_form"):

        name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        phone = st.text_input("Phone Number")

        experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=0
        )

        role = st.text_input("Desired Position")

        location = st.text_input("Current Location")

        tech_stack = st.text_area(
            "Tech Stack (Python, SQL, React, Machine Learning etc.)"
        )

        submitted = st.form_submit_button("Start Screening")

    # --------------------------------
    # FORM VALIDATION
    # --------------------------------
    if submitted:

        if not validate_email(email):

            st.error("❌ Please enter a valid email address.")

        elif not validate_phone(phone):

            st.error("❌ Please enter a valid 10-digit phone number.")

        elif tech_stack.strip() == "":

            st.error("❌ Please enter your tech stack.")

        else:

            st.session_state.candidate = {
                "name": name,
                "email": email,
                "phone": phone,
                "experience": experience,
                "role": role,
                "location": location,
                "tech_stack": tech_stack
            }

            # 🧠 Generate AI Questions
            st.session_state.questions = generate_questions(tech_stack)

            st.session_state.stage = "questions"

            st.rerun()

# --------------------------------
# STAGE 2 : TECHNICAL QUESTIONS
# --------------------------------
elif st.session_state.stage == "questions":

    st.success("✅ Profile received successfully.")

    st.subheader("🧠 Technical Assessment")

    with st.form("answers_form"):

        for index, question in enumerate(
            st.session_state.questions,
            start=1
        ):

            st.write(f"### {index}. {question}")

            st.text_area(
                "Your Answer",
                key=f"answer_{index}"
            )

        final_submit = st.form_submit_button("Submit Answers")

    # --------------------------------
    # ANSWER EVALUATION
    # --------------------------------
    if final_submit:

        results = []

        total_score = 0

        for index, question in enumerate(
            st.session_state.questions,
            start=1
        ):

            answer = st.session_state.get(
                f"answer_{index}",
                ""
            ).strip()

            # ❌ Empty Answer
            if answer == "":

                result = {
                    "score": 0,
                    "feedback": "No answer submitted by candidate.",
                    "result": "Unanswered"
                }

            # 🧠 AI + Fallback Evaluation
            else:

                result = evaluate_answer(
                    question,
                    answer,
                    index=index
                )

            total_score += int(result["score"])

            results.append({
                "question": question,
                "answer": answer,
                **result
            })

        # 📊 Store Results
        st.session_state.candidate["results"] = results

        st.session_state.candidate["score"] = total_score

        # 💾 Save Candidate Data
        save_candidate(st.session_state.candidate)

        st.session_state.stage = "result"

        st.rerun()

# --------------------------------
# STAGE 3 : FINAL RESULT
# --------------------------------
elif st.session_state.stage == "result":

    candidate = st.session_state.candidate

    results = candidate["results"]

    st.subheader("📊 Candidate Evaluation Report")

    # --------------------------------
    # SHOW RESULTS
    # --------------------------------
    for index, item in enumerate(results, start=1):

        st.write(f"### Question {index}")

        st.write(f"**Q:** {item['question']}")

        st.write(f"**Score:** {item['score']}/10")

        st.write(f"**Feedback:** {item['feedback']}")

        st.markdown("---")

    # --------------------------------
    # FINAL SCORE
    # --------------------------------
    max_score = len(results) * 10

    final_score = candidate["score"]

    st.success(f"🎯 Final Score: {final_score}/{max_score}")

    # --------------------------------
    # FINAL DECISION
    # --------------------------------
    if final_score >= max_score * 0.7:

        st.success("✅ Recommended for Next Round")

    else:

        st.warning("⚠️ Needs Improvement")

    st.info(
        "Thank you for completing the TalentScout assessment."
    )

    # --------------------------------
    # RESET APP
    # --------------------------------
    if st.button("Start New Candidate"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
