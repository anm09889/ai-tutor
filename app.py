import streamlit as st
import random

# =========================
# QUIZ DATA
# =========================
def generate_quiz(topic):
    return [
        {
            "question": f"What is {topic}?",
            "options": [
                "Technique to solve problems",
                "A sorting algorithm",
                "A database type",
                "A hardware device"
            ],
            "answer": "Technique to solve problems"
        },
        {
            "question": f"Where is {topic} used?",
            "options": [
                "Problem solving",
                "Only hardware",
                "Only networks",
                "Only OS"
            ],
            "answer": "Problem solving"
        },
        {
            "question": f"What is main idea of {topic}?",
            "options": [
                "Break problem into subproblems",
                "Delete data",
                "Sort arrays",
                "Encrypt files"
            ],
            "answer": "Break problem into subproblems"
        },
        {
            "question": f"{topic} improves what?",
            "options": [
                "Efficiency",
                "Hardware speed",
                "Internet speed",
                "Screen brightness"
            ],
            "answer": "Efficiency"
        },
        {
            "question": f"{topic} is mostly used in?",
            "options": [
                "Algorithms",
                "Gaming only",
                "Photoshop",
                "Music apps"
            ],
            "answer": "Algorithms"
        }
    ]

# =========================
# SESSION STATE INIT
# =========================
if "quiz" not in st.session_state:
    st.session_state.quiz = []
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.started = False

# =========================
# UI
# =========================
st.title("📝 Smart Quiz System")

topic = st.text_input("Enter topic for quiz")

# =========================
# START QUIZ
# =========================
if st.button("Start Quiz"):

    if topic:
        st.session_state.quiz = generate_quiz(topic)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.started = True
    else:
        st.warning("Enter a topic")

# =========================
# QUIZ LOGIC
# =========================
if st.session_state.started:

    quiz = st.session_state.quiz
    i = st.session_state.q_index

    if i < len(quiz):

        q = quiz[i]

        st.subheader(f"Q{i+1}: {q['question']}")

        selected = st.radio(
            "Choose your answer",
            q["options"],
            key=f"option_{i}"
        )

        if st.button("Next"):

            if selected == q["answer"]:
                st.session_state.score += 1

            st.session_state.q_index += 1
            st.rerun()

    else:
        st.success(f"🎉 Quiz Completed! Your Score: {st.session_state.score}/{len(quiz)}")

        if st.button("Restart Quiz"):
            st.session_state.started = False
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.quiz = []
            st.rerun()
