import streamlit as st
import random

# =========================
# PAGE CONFIG (MUST BE FIRST UI CALL)
# =========================
st.set_page_config(page_title="AI Tutor", layout="wide")

# =========================
# HEADER (FORCE UI TO APPEAR)
# =========================
st.title("🧠 AI Learning Tutor")
st.write("Ask any question — get simple, smart explanation instantly")

# =========================
# SAFE AI ENGINE
# =========================
def ai_engine(q):

    q = q.lower()

    answers = [
        f"{q} is an important concept in computer science. It helps in understanding core principles step-by-step.",
        f"Let’s break it down: {q} is used to solve real-world problems using logical thinking.",
        f"{q} can be understood by learning its definition, working, and real-life application.",
        f"Simple explanation: {q} is a fundamental idea used in programming and system design."
    ]

    return random.choice(answers)

# =========================
# INPUT BOX
# =========================
question = st.text_input("💬 Ask your question")

# =========================
# BUTTON (MAIN TRIGGER)
# =========================
if st.button("Get Answer"):

    if question.strip() != "":
        with st.spinner("Thinking..."):
            answer = ai_engine(question)

        st.success("Answer generated:")
        st.write(answer)

    else:
        st.warning("Please enter a question")

# =========================
# FOOTER (ENSURES UI ALWAYS LOADS)
# =========================
st.markdown("---")
st.write("✔ System Active | AI Tutor Running")
