import streamlit as st
import random
import graphviz

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Learning System",
    page_icon="🎓",
    layout="wide"
)

# =========================
# UI HEADER
# =========================
st.markdown("""
    <h1 style='text-align:center; color:#4F8BF9;'>🎓 AI Learning System</h1>
    <p style='text-align:center; color:gray;'>Smart Tutor • MCQ Quiz • Visual Learning</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "started" not in st.session_state:
    st.session_state.started = False
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# AI TUTOR (NO API)
# =========================
def ai_tutor(topic):

    return f"""
📘 Topic: {topic}

✔ Core Concept:
{topic} is an important concept in Computer Science used for solving structured computational problems.

✔ Explanation:
It focuses on efficient design, optimization, and structured problem-solving approaches.

✔ Real-world Usage:
- Software development  
- System design  
- Databases  
- Algorithms  

✔ Key Idea:
Understanding time complexity and logical structure is important.

✔ Tip:
Focus on understanding *why* it works, not just memorizing it.
"""

# =========================
# MEDIUM LEVEL QUIZ (IMPROVED OPTIONS)
# =========================
def generate_quiz(topic):

    return [
        {
            "q": f"What is the primary goal of {topic}?",
            "options": [
                "Efficient problem solving",
                "Decorative coding style",
                "Random output generation",
                "Memory formatting"
            ],
            "ans": "Efficient problem solving"
        },
        {
            "q": f"{topic} is most closely related to which area?",
            "options": [
                "Data Structures & Algorithms",
                "Graphic Design",
                "Music Production",
                "Civil Engineering"
            ],
            "ans": "Data Structures & Algorithms"
        },
        {
            "q": f"What is an important factor in analyzing {topic}?",
            "options": [
                "Time and Space Complexity",
                "Color combination",
                "Font size",
                "Animation speed"
            ],
            "ans": "Time and Space Complexity"
        },
        {
            "q": f"{topic} helps in improving which system property?",
            "options": [
                "Efficiency",
                "Decoration",
                "Sound quality",
                "Brightness"
            ],
            "ans": "Efficiency"
        },
        {
            "q": f"Which concept is often used with {topic}?",
            "options": [
                "Recursion and iteration",
                "Painting tools",
                "Audio mixing",
                "Video editing"
            ],
            "ans": "Recursion and iteration"
        }
    ]

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Quiz", "📊 Visual Learning"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("Ask Your Topic")

    topic = st.text_input("Enter topic (e.g., Quick Sort, DBMS, OS)")

    if st.button("Generate Explanation"):
        if topic:
            st.info(ai_tutor(topic))
            st.session_state.history.append(topic)

    st.write("Recent Topics:")
    st.write(st.session_state.history[-5:])

# =========================
# 📝 QUIZ (FIXED + MEDIUM LEVEL)
# =========================
elif menu == "📝 Quiz":

    st.subheader("MCQ Quiz System (Medium Level)")

    topic = st.text_input("Enter topic for quiz")

    if st.button("Start Quiz") and topic:
        st.session_state.quiz = generate_quiz(topic)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.started = True

    if st.session_state.started:

        i = st.session_state.q_index
        quiz = st.session_state.quiz

        if i < len(quiz):

            qdata = quiz[i]

            st.markdown(f"### Q{i+1}: {qdata['q']}")

            answer = st.radio(
                "Choose correct answer",
                qdata["options"],
                key=f"q_{i}"
            )

            if st.button("Next Question"):

                if answer == qdata["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎯 Final Score: {st.session_state.score}/5")

            if st.button("Restart Quiz"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.rerun()

# =========================
# 📊 VISUAL LEARNING (FLOWCHART ONLY)
# =========================
elif menu == "📊 Visual Learning":

    st.subheader("Concept Visualization")

    topic = st.text_input("Enter topic for visualization")

    if st.button("Generate Flowchart"):

        if topic:

            st.markdown("### 🔁 Concept Flow")

            dot = graphviz.Digraph()

            dot.node("A", topic)
            dot.node("B", "Definition")
            dot.node("C", "Working Mechanism")
            dot.node("D", "Applications")
            dot.node("E", "Complexity Analysis")

            dot.edges([
                ("A", "B"),
                ("A", "C"),
                ("C", "D"),
                ("C", "E")
            ])

            st.graphviz_chart(dot)
