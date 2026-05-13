import streamlit as st
import random
import graphviz
from transformers import pipeline

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="College AI Tutor",
    page_icon="🎓",
    layout="wide"
)

# =========================
# LOAD AI MODEL
# =========================
@st.cache_resource
def load_ai():
    return pipeline("text-generation", model="gpt2")

ai = load_ai()

# =========================
# UI HEADER
# =========================
st.markdown("""
    <h1 style='text-align:center; color:#4F8BF9;'>🎓 College AI Tutor</h1>
    <p style='text-align:center; color:gray;'>DSA • DBMS • OS • CN • AI Learning System</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key in ["score", "q_index", "quiz", "started", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else 0 if key in ["score","q_index"] else False if key=="started" else []

# =========================
# 🧠 AI EXPLANATION ENGINE
# =========================
def explain_topic(topic, mode):

    prompt = f"""
Explain {topic} for college students.

Mode: {mode}

Include:
- Definition
- Working
- Real-world use cases
- Exam importance
- Key points
"""

    result = ai(prompt, max_length=220, do_sample=True)[0]["generated_text"]

    return result

# =========================
# 📝 SMART QUIZ GENERATOR
# =========================
def generate_options(correct):

    base = [
        "Stack based approach",
        "Queue mechanism",
        "Hashing technique",
        "Recursive strategy",
        "Greedy method",
        "Divide and Conquer",
        "Dynamic Programming"
    ]

    base = list(set(base + [correct]))
    random.shuffle(base)

    return base[:4]


def generate_quiz(topic):

    return [
        {
            "q": f"Which best describes {topic}?",
            "ans": "Problem Solving Technique",
            "options": generate_options("Problem Solving Technique")
        },
        {
            "q": f"What is main idea of {topic}?",
            "ans": "Efficient Computation",
            "options": generate_options("Efficient Computation")
        },
        {
            "q": f"{topic} is used in which field?",
            "ans": "Computer Science",
            "options": generate_options("Computer Science")
        },
        {
            "q": f"Key factor in {topic}?",
            "ans": "Time Complexity",
            "options": generate_options("Time Complexity")
        },
        {
            "q": f"{topic} improves which system property?",
            "ans": "Performance",
            "options": generate_options("Performance")
        }
    ]

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Exam Mode", "📊 Learning Path"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("Smart Explanation System")

    topic = st.text_input("Enter topic (DSA / OS / DBMS / CN)")

    mode = st.selectbox("Learning Mode", ["Beginner", "Exam", "Interview"])

    if st.button("Generate Explanation"):

        if topic:
            st.session_state.history.append(topic)

            st.success(explain_topic(topic, mode))

# =========================
# 📝 EXAM MODE
# =========================
elif menu == "📝 Exam Mode":

    st.subheader("College-Level MCQ Exam")

    topic = st.text_input("Enter topic")

    if st.button("Start Exam") and topic:
        st.session_state.quiz = generate_quiz(topic)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.started = True

    if st.session_state.started:

        i = st.session_state.q_index
        quiz = st.session_state.quiz

        if i < len(quiz):

            q = quiz[i]

            st.markdown(f"### Q{i+1}: {q['q']}")

            answer = st.radio(
                "Choose answer",
                q["options"],
                key=f"q_{i}"
            )

            if st.button("Next Question"):

                if answer == q["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎯 Final Score: {st.session_state.score}/5")

            st.progress(st.session_state.score / 5)

            if st.button("Restart Exam"):
                st.session_state.started = False
                st.rerun()

# =========================
# 📊 LEARNING PATH VISUALIZER
# =========================
elif menu == "📊 Learning Path":

    st.subheader("Concept Understanding Flow")

    topic = st.text_input("Enter topic")

    if st.button("Generate Path"):

        if topic:

            dot = graphviz.Digraph()

            dot.node("A", topic)
            dot.node("B", "Definition")
            dot.node("C", "Working")
            dot.node("D", "Applications")
            dot.node("E", "Complexity Analysis")
            dot.node("F", "Interview Importance")

            dot.edges([
                ("A","B"),
                ("A","C"),
                ("C","D"),
                ("C","E"),
                ("C","F")
            ])

            st.graphviz_chart(dot)

    st.info("Use this to understand how concepts connect in real exams and interviews.")
