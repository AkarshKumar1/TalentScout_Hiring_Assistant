# 🤖 TalentScout AI Hiring Assistant

An AI-powered hiring assistant built using **Python**, **Streamlit**, and **Google Gemini API** for initial candidate screening.
The application helps recruiters automate the first round of hiring by collecting candidate details, generating technical questions based on the candidate’s tech stack, evaluating responses using AI, and producing a final assessment report.

---

# 📌 Project Overview

TalentScout AI Hiring Assistant is designed for recruitment agencies and HR teams to simplify the early-stage screening process.

Instead of manually interviewing every applicant, the assistant:

* Collects candidate profile details
* Generates skill-based technical questions
* Accepts candidate answers
* Uses AI to evaluate answers
* Provides a score and hiring recommendation

This project demonstrates practical use of **LLMs in recruitment workflows**.

---

# 🚀 Features

## ✅ Candidate Information Collection

The system collects:

* Full Name
* Email Address
* Phone Number
* Years of Experience
* Desired Position
* Current Location
* Tech Stack

---

## ✅ AI-Based Technical Question Generation

Based on the candidate's declared skills, the system generates technical interview questions for technologies such as:

* Python
* SQL / MySQL
* React
* Machine Learning
* Custom technologies

---

## ✅ AI Answer Evaluation

Candidate responses are analyzed using **Google Gemini API**, which provides:

* Score out of 10 for each question
* Feedback for each answer
* Final total score
* Recommendation for next round

---

## ✅ Result Dashboard

After assessment, the system shows:

* Individual question scores
* AI feedback
* Final score
* Needs Improvement / Recommended status

---

## ✅ Data Storage

All candidate responses and scores are stored locally in:

```text
data/candidates.json
```

---

# 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **JSON**
* **dotenv**

---

# 📂 Updated Folder Structure

```text
TalentScout_Hiring_Assistant/
│── app.py
│── requirements.txt
│── README.md
│── .env
│── .gitignore
│── data/
│   └── candidates.json
│── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── storage.py
│   ├── llm.py
│   └── prompts.py
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <your-github-repo-link>
cd TalentScout_Hiring_Assistant
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Add API Key

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 4️⃣ Run Application

```bash
streamlit run app.py
```

---

# 🌐 Deployment (Streamlit Cloud)

This project can be deployed on **Streamlit Community Cloud**.

Steps:

1. Push project to GitHub
2. Open Streamlit Cloud
3. Connect GitHub repository
4. Select `app.py`
5. Add secret:

```toml
GEMINI_API_KEY="your_api_key_here"
```

---

# 🧠 Prompt Engineering Used

## Question Generation Prompt

The assistant uses prompts to generate technical interview questions according to the candidate's declared tech stack.

## Answer Evaluation Prompt

The assistant evaluates candidate answers using AI and returns:

* Score
* Feedback
* Correctness level

---

# 🔐 Data Privacy

* Candidate data is stored locally for demo purposes.
* No personal data is shared externally except AI evaluation requests.
* API keys are stored securely using `.env` or Streamlit Secrets.

---

# ⚠️ Challenges Solved

During development, the following challenges were addressed:

* Streamlit rerun issues using `session_state`
* Dynamic multi-step workflow
* Gemini API integration
* AI response parsing
* Blank answer handling
* Candidate data storage

---

# 📈 Future Improvements

* Resume Upload Feature
* Recruiter Admin Dashboard
* PDF Report Export
* Candidate Ranking System
* Multi-language Support
* Email Notifications

---

# 👨‍💻 Author

**Akarsh Kumar**

B.Tech CSE (AI/ML) Student
Passionate about AI, Machine Learning, and Real-World Product Development.

---

# ⭐ Final Note

This project was developed as part of an AI/ML Internship Assignment to demonstrate practical implementation of LLM-powered hiring automation.
