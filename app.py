import streamlit as st
import graphviz
from transformers import pipeline

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Tutor Pro (Industry)",
    page_icon="🎓",
    layout="wide"
)

# =========================
# LOAD REAL AI MODEL (FAST + FREE)
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

model = load_model()

# =========================
# UI HEADER
# =========================
st.markdown("""
    <h1 style='text-align:center; color:#4F8BF9;'>🎓 AI Tutor Pro - Industry Level</h1>
    <p style='text-align:center; color:gray;'>AI Tutor • Smart Quiz • Learning Path • Visualization</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key in ["score", "q_index", "quiz", "started"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key == "score" or key == "q_index" else [] if key == "quiz" else False

# =========================
# 🧠 REAL AI ANSWER ENGINE
# =========================
def ai_answer(topic, level):

    prompt = f"""
Explain the topic in detail.

Topic: {topic}
Level: {level}

Include:
- Definition
- Working
- Real-world use cases
- Complexity or importance
"""

    result = model(prompt, max_length=200, do_sample=True)[0]["generated_text"]

    return result

# =========================
# 📝 QUIZ GENERATOR (INDUSTRY LEVEL)
# =========================
def generate_quiz(topic, level):

    base = [
        {
            "q": f"What best describes {topic}?",
            "options": [
                "A structured problem-solving technique",
                "A graphical design tool",
                "A music system",
                "A hardware component"
            ],
            "ans": "A structured problem-solving technique"
        },
        {
            "q": f"Which concept is essential in analyzing {topic}?",
            "options": [
                "Time and Space Complexity",
                "Color grading",
                "Audio signals",
                "Pixel rendering"
            ],
            "ans": "Time and Space Complexity"
        },
        {
            "q": f"{topic} is mainly used in?",
            "options": [
                "Algorithm design",
                "Video editing",
                "Game graphics",
                "Photography"
            ],
            "ans": "Algorithm design"
        },
        {
            "q": f"What improves performance in {topic}?",
            "options": [
                "Optimization techniques",
                "Increasing size",
                "Adding colors",
                "Using images"
            ],
            "ans": "Optimization techniques"
        },
        {
            "q": f"{topic} often involves?",
            "options": [
                "Logical reasoning",
                "Painting skills",
                "Sound mixing",
                "Animation"
            ],
            "ans": "Logical reasoning"
        }
    ]

    return base if level == "Medium" else base

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Quiz Engine", "📊 Learning Visualizer"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("AI Learning Assistant")

    topic = st.text_input("Enter topic (DSA, OS, DBMS, etc.)")

    level = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Explanation"):

        if topic:
            response = ai_answer(topic, level)
            st.success(response)

# =========================
# 📝 QUIZ ENGINE
# =========================
elif menu == "📝 Quiz Engine":

    st.subheader("Smart MCQ Assessment System")

    topic = st.text_input("Enter topic")
    level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Start Quiz") and topic:
        st.session_state.quiz = generate_quiz(topic, level)
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
                "Select Answer",
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

            if st.button("Restart"):
                st.session_state.started = False
                st.rerun()

# =========================
# 📊 VISUAL LEARNING SYSTEM
# =========================
elif menu == "📊 Learning Visualizer":

    st.subheader("Concept Learning Flow")

    topic = st.text_input("Enter topic")

    if st.button("Generate Learning Path"):

        if topic:

            st.markdown("### 🔁 Knowledge Flow")

            dot = graphviz.Digraph()

            dot.node("A", topic)
            dot.node("B", "Definition")
            dot.node("C", "Working Principle")
            dot.node("D", "Applications")
            dot.node("E", "Optimization")

            dot.edges([
                ("A", "B"),
                ("A", "C"),
                ("C", "D"),
                ("C", "E")
            ])

            st.graphviz_chart(dot)
