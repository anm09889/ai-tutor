import streamlit as st
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SIMPLE FAST AI (NO SLOW MODEL)
# =========================
def ai_tutor(question):
    return f"""
📘 ANSWER:

{question}

✔ Definition:
This is an important concept in Computer Science.

✔ Explanation:
It is used to solve problems efficiently by breaking them into steps.

✔ Example:
Used in algorithms, apps, search engines, and AI systems.

✔ Key Idea:
Focus on optimization and structured thinking.

✔ Tip:
Always understand the logic, not just memorization.
"""

# =========================
# QUIZ GENERATOR
# =========================
def generate_quiz(topic):
    return [
        (f"What is {topic}?", "Concept"),
        (f"Where is {topic} used?", "Algorithms"),
        (f"Why is {topic} important?", "Efficiency"),
        (f"Explain {topic} in simple terms", "Steps"),
        (f"{topic} belongs to which field?", "CS")
    ]

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
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio("📌 MENU", ["🤖 AI Tutor", "📝 Quiz", "🧰 Tools", "📊 Analysis"])

# =========================
# 🤖 AI TUTOR SECTION
# =========================
if menu == "🤖 AI Tutor":

    st.title("🎓 AI Tutor Pro")

    question = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                answer = ai_tutor(question)
                st.success(answer)

                st.session_state.history.append(question)
        else:
            st.warning("Enter a question")

    st.subheader("📌 Recent Questions")
    st.write(st.session_state.history[-5:])

# =========================
# 📝 QUIZ SECTION
# =========================
elif menu == "📝 Quiz":

    st.title("📝 Smart Quiz System")

    topic = st.text_input("Enter topic for quiz")

    if st.button("Start Quiz"):
        if topic:
            st.session_state.quiz = generate_quiz(topic)
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.started = True

    if st.session_state.started:

        q_data = st.session_state.quiz
        i = st.session_state.q_index

        if i < len(q_data):

            q, correct = q_data[i]

            st.subheader(f"Q{i+1}: {q}")

            options = ["Concept", "Algorithms", "Efficiency", "Steps"]
            answer = st.radio("Choose answer", options, key=i)

            if st.button("Next"):

                if answer == correct:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎉 Final Score: {st.session_state.score}/5")

            if st.button("Restart Quiz"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.rerun()

# =========================
# 🧰 TOOLS SECTION
# =========================
elif menu == "🧰 Tools":

    st.title("🧰 Study Tools")

    tool = st.selectbox("Choose Tool", [
        "Quick Notes Maker",
        "Study Timer",
        "Simple Calculator"
    ])

    if tool == "Quick Notes Maker":
        text = st.text_area("Write topic")
        if st.button("Generate Notes"):
            st.info(f"📘 Summary:\n\n{text} is an important CS concept used in problem solving.")

    elif tool == "Study Timer":
        minutes = st.number_input("Set minutes", 1, 60, 5)
        if st.button("Start Timer"):
            st.success(f"Timer started for {minutes} minutes (simulate)")

    elif tool == "Simple Calculator":
        a = st.number_input("A")
        b = st.number_input("B")
        op = st.selectbox("Operation", ["Add", "Subtract", "Multiply"])

        if st.button("Calculate"):
            if op == "Add":
                st.success(a + b)
            elif op == "Subtract":
                st.success(a - b)
            else:
                st.success(a * b)

# =========================
# 📊 ANALYSIS SECTION
# =========================
elif menu == "📊 Analysis":

    st.title("📊 Student Analysis")

    st.metric("Total Questions Asked", len(st.session_state.history))
    st.metric("Quiz Score", st.session_state.score)

    st.write("Recent Activity:")
    st.write(st.session_state.history[-10:])
