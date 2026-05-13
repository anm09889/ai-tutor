import streamlit as st
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Tutor Pro System",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "scores" not in st.session_state:
    st.session_state.scores = []
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# =========================
# AI TUTOR (SIMPLE OFFLINE AI)
# =========================
def ai_response(question):
    return f"""
📘 Explanation of: {question}

1. Definition:
This is an important concept in computer science.

2. Idea:
It works by breaking problems into smaller parts.

3. Example:
Used in real-world systems like Google search, apps, and games.

4. Complexity:
Depends on the problem type (usually optimized using algorithms).

5. Advantage:
Improves efficiency and performance.

6. Disadvantage:
Can be complex for beginners.
"""

# =========================
# QUIZ GENERATOR
# =========================
def generate_quiz(topic):
    return [
        {
            "question": f"What is {topic}?",
            "options": [
                "Problem solving technique",
                "Hardware device",
                "Operating system",
                "Network protocol"
            ],
            "answer": "Problem solving technique"
        },
        {
            "question": f"Where is {topic} used?",
            "options": [
                "Algorithms",
                "Only hardware",
                "Only UI design",
                "Only databases"
            ],
            "answer": "Algorithms"
        },
        {
            "question": f"Main idea of {topic}?",
            "options": [
                "Divide and solve problems",
                "Store images",
                "Print documents",
                "Manage memory only"
            ],
            "answer": "Divide and solve problems"
        },
        {
            "question": f"{topic} improves?",
            "options": [
                "Efficiency",
                "Screen brightness",
                "Internet speed only",
                "Keyboard input"
            ],
            "answer": "Efficiency"
        },
        {
            "question": f"{topic} is related to?",
            "options": [
                "Computer science",
                "Cooking",
                "Music",
                "Painting"
            ],
            "answer": "Computer science"
        }
    ]

# =========================
# SIDEBAR NAVIGATION
# =========================
menu = st.sidebar.radio(
    "📌 MENU",
    ["🤖 AI Tutor", "📝 Quiz", "📊 Analysis"]
)

# =========================
# 🤖 AI TUTOR SECTION
# =========================
if menu == "🤖 AI Tutor":

    st.title("🤖 AI Tutor Section")

    question = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if question:
            st.success(ai_response(question))
        else:
            st.warning("Please enter a question")

# =========================
# 📝 QUIZ SECTION
# =========================
elif menu == "📝 Quiz":

    st.title("📝 Quiz Section")

    topic = st.text_input("Enter topic for quiz")

    if "quiz" not in st.session_state:
        st.session_state.quiz = []
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.started = False

    if st.button("Start Quiz"):
        if topic:
            st.session_state.quiz = generate_quiz(topic.lower())
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.started = True
        else:
            st.warning("Enter a topic")

    if st.session_state.get("started", False):

        quiz = st.session_state.quiz
        i = st.session_state.q_index

        if i < len(quiz):

            q = quiz[i]

            st.subheader(f"Q{i+1}: {q['question']}")

            selected = st.radio(
                "Choose answer",
                q["options"],
                key=f"q_{i}"
            )

            if st.button("Next"):

                if selected == q["answer"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎉 Score: {st.session_state.score}/5")

            st.session_state.scores.append(st.session_state.score)
            st.session_state.attempts += 1

            if st.button("Restart Quiz"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.quiz = []
                st.rerun()

# =========================
# 📊 ANALYSIS SECTION
# =========================
elif menu == "📊 Analysis":

    st.title("📊 Student Performance Analysis")

    if st.session_state.attempts == 0:
        st.info("No quiz attempts yet")
    else:
        avg = sum(st.session_state.scores) / len(st.session_state.scores)

        st.metric("Total Attempts", st.session_state.attempts)
        st.metric("Average Score", round(avg, 2))

        st.line_chart(st.session_state.scores)

        st.write("Score History:", st.session_state.scores)
