import streamlit as st
import random
import graphviz
from transformers import pipeline

# =========================
# APP CONFIG
# =========================
st.set_page_config(
    page_title="AI EdTech Platform",
    page_icon="🎓",
    layout="wide"
)

# =========================
# LOAD AI MODEL
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

ai = load_model()

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align:center; color:#4F8BF9;'>🎓 AI EdTech Platform</h1>
<p style='text-align:center; color:gray;'>Tutor • Exam • Interview • Analytics • Concept Mapping</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key in ["score", "q_index", "quiz", "started", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else 0 if key in ["score","q_index"] else False if key=="started" else []

# =========================
# AI ENGINE
# =========================
def ai_response(topic, mode):

    prompt = f"""
Explain {topic} for students.

Mode: {mode}

Include:
- Definition
- Working
- Real-world use
- Interview importance
- Exam answer format
"""

    result = ai(prompt, max_length=220, do_sample=True)[0]["generated_text"]

    return result

# =========================
# EXAM QUESTIONS (MEDIUM LEVEL)
# =========================
def generate_quiz(topic):

    return [
        {
            "q": f"What is the core idea of {topic}?",
            "options": [
                "Efficient problem solving",
                "Random execution",
                "Visual design",
                "Hardware optimization"
            ],
            "ans": "Efficient problem solving"
        },
        {
            "q": f"{topic} is mainly used in?",
            "options": [
                "Algorithms & Data Structures",
                "Graphic Design",
                "Video Editing",
                "Networking hardware"
            ],
            "ans": "Algorithms & Data Structures"
        },
        {
            "q": f"Key factor in analyzing {topic}?",
            "options": [
                "Time and Space Complexity",
                "Color grading",
                "Audio frequency",
                "Image resolution"
            ],
            "ans": "Time and Space Complexity"
        },
        {
            "q": f"{topic} improves which system property?",
            "options": [
                "Performance",
                "Decoration",
                "Sound",
                "Brightness"
            ],
            "ans": "Performance"
        },
        {
            "q": f"{topic} is related to?",
            "options": [
                "Logical reasoning",
                "Painting",
                "Music",
                "Animation"
            ],
            "ans": "Logical reasoning"
        }
    ]

# =========================
# SIDEBAR NAVIGATION
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Exam Mode", "🎯 Interview Mode", "🔁 Concept Map", "📊 Analytics"]
)

# =========================
# 🤖 AI TUTOR MODULE
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("Smart AI Tutor Engine")

    topic = st.text_input("Enter topic (DSA, OS, DBMS, CN, AI)")

    mode = st.selectbox("Mode", ["Beginner", "Intermediate", "Advanced", "Interview", "Exam Answer"])

    if st.button("Generate Explanation"):

        if topic:
            st.session_state.history.append(topic)
            st.success(ai_response(topic, mode))

    st.write("Recent Topics:")
    st.write(st.session_state.history[-5:])

# =========================
# 📝 EXAM MODE
# =========================
elif menu == "📝 Exam Mode":

    st.subheader("College-Level MCQ Exam System")

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
                "Select answer",
                q["options"],
                key=f"q_{i}"
            )

            if st.button("Next"):

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
# 🎯 INTERVIEW MODE
# =========================
elif menu == "🎯 Interview Mode":

    st.subheader("Interview Preparation Mode")

    topic = st.text_input("Enter topic")

    if st.button("Generate Interview Answer"):

        if topic:
            st.info(ai_response(topic, "Interview"))

# =========================
# 🔁 CONCEPT MAP
# =========================
elif menu == "🔁 Concept Map":

    st.subheader("Concept Relationship Graph")

    topic = st.text_input("Enter topic")

    if st.button("Generate Map"):

        if topic:

            dot = graphviz.Digraph()

            dot.node("A", topic)
            dot.node("B", "Core Idea")
            dot.node("C", "Working Principle")
            dot.node("D", "Applications")
            dot.node("E", "Complexity / Importance")
            dot.node("F", "Related Concepts")

            dot.edges([
                ("A","B"),
                ("A","C"),
                ("C","D"),
                ("C","E"),
                ("C","F")
            ])

            st.graphviz_chart(dot)

# =========================
# 📊 ANALYTICS
# =========================
elif menu == "📊 Analytics":

    st.subheader("Student Learning Analytics")

    st.metric("Topics Studied", len(st.session_state.history))
    st.metric("Last Score", st.session_state.score)

    st.progress(min(st.session_state.q_index / 5, 1.0))

    st.write("Recent Topics:")
    st.write(st.session_state.history[-10:])
