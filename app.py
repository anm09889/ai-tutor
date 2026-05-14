import streamlit as st
import time
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Learning Studio",
    page_icon="🎓",
    layout="wide"
)

# =========================
# MODERN UI STYLE (CUSTOM CSS)
# =========================
st.markdown("""
<style>

body {
    background-color: #0f172a;
    color: white;
}

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #38bdf8;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
}

button {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# =========================
# FAST AI ENGINE
# =========================
def ai_answer(question):
    q = question.lower()

    if "sorting" in q:
        return "Sorting arranges data in order. Example: Bubble, Merge, Quick Sort. Time complexity varies from O(n²) to O(n log n)."

    if "dp" in q or "dynamic programming" in q:
        return "Dynamic Programming solves problems by storing results of subproblems to avoid repetition. It improves efficiency drastically."

    if "array" in q:
        return "Array is a linear data structure storing elements in contiguous memory. Access is O(1)."

    return f"Simple Explanation:\n\n{question}\n\nThis concept is used in Computer Science for problem solving and optimization."

# =========================
# QUIZ GENERATOR
# =========================
def quiz(topic):
    return [
        (f"What is {topic}?", "Concept"),
        (f"Why is {topic} used?", "Efficiency"),
        (f"Where is {topic} applied?", "CS"),
        (f"Main idea of {topic}?", "Logic"),
        (f"{topic} belongs to?", "Computer Science")
    ]

# =========================
# HEADER UI
# =========================
st.markdown("<div class='main-title'>🎓 AI Learning Studio</div>", unsafe_allow_html=True)
st.write("Smart AI Tutor + Quiz System + Student Analysis")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🤖 Tutor", "📝 Quiz", "📊 Analysis"])

# =========================
# 🤖 TUTOR
# =========================
with tab1:
    st.markdown("### 🤖 AI Tutor")

    question = st.text_input("Ask anything (DSA, DBMS, OS, AI)")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                ans = ai_answer(question)

            st.markdown(f"""
            <div class="card">
            {ans}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question")

# =========================
# 📝 QUIZ
# =========================
with tab2:
    st.markdown("### 📝 Smart Quiz System")

    topic = st.text_input("Enter topic for quiz")

    if st.button("Start Quiz"):
        if topic:
            st.session_state.quiz_data = quiz(topic)
            st.session_state.quiz_started = True
            st.session_state.q_index = 0
            st.session_state.score = 0

    if st.session_state.quiz_started:

        q_data = st.session_state.quiz_data
        i = st.session_state.q_index

        if i < len(q_data):

            q, correct = q_data[i]

            st.markdown(f"""
            <div class="card">
            <h3>Q{i+1}: {q}</h3>
            </div>
            """, unsafe_allow_html=True)

            options = ["Concept", "Efficiency", "CS", "Logic", "Computer Science"]
            answer = st.radio("Choose answer", options, key=i)

            if st.button("Next Question"):

                if answer == correct:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎉 Final Score: {st.session_state.score}/5")

            if st.button("Restart Quiz"):
                st.session_state.quiz_started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.rerun()

# =========================
# 📊 ANALYSIS
# =========================
with tab3:
    st.markdown("### 📊 Student Analysis")

    st.metric("Quiz Score", st.session_state.score)
    st.metric("Questions Attempted", st.session_state.q_index)

    st.write("Progress Tracker")
    st.progress(min(st.session_state.q_index / 5, 1.0))
