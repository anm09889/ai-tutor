import streamlit as st
from transformers import pipeline
import random
import time

# =========================
# PAGE CONFIG (UI IMPROVED)
# =========================
st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide"
)

# =========================
# FAST AI MODEL LOADER
# =========================
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )

generator = load_model()

# =========================
# SESSION STATE (STUDENT ANALYSIS)
# =========================
if "scores" not in st.session_state:
    st.session_state.scores = []
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# =========================
# SIMPLE QUESTION GENERATOR (NO API KEY)
# =========================
def generate_quiz(topic):
    base_questions = [
        f"What is {topic}?",
        f"Explain the main idea of {topic}.",
        f"Where is {topic} used?",
        f"What are advantages of {topic}?",
        f"What is time complexity related to {topic}?"
    ]

    quiz = []
    for q in base_questions:
        quiz.append({
            "question": q,
            "options": [
                "Correct concept explanation",
                "Wrong answer A",
                "Wrong answer B",
                "Wrong answer C"
            ],
            "answer": "Correct concept explanation"
        })

    return quiz

# =========================
# AI ANSWER FUNCTION
# =========================
def get_ai_answer(question):
    prompt = f"""
You are an expert DSA tutor.

Explain clearly:
- Definition
- Steps
- Example
- Real-life use

Question: {question}
Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True,
        repetition_penalty=1.2
    )

    return result[0]["generated_text"].replace(prompt, "")

# =========================
# UI DESIGN (MODERN)
# =========================
st.title("🎓 AI Tutor Pro (Smart Learning System)")

tab1, tab2, tab3 = st.tabs(["💬 AI Tutor", "📝 Quiz", "📊 Student Analysis"])

# =========================
# TAB 1 - AI TUTOR
# =========================
with tab1:
    st.subheader("Ask Anything")

    question = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                answer = get_ai_answer(question)
                st.success(answer)
        else:
            st.warning("Please enter a question")

# =========================
# TAB 2 - QUIZ SYSTEM
# =========================
with tab2:
    st.subheader("Topic-Based Quiz Generator")

    topic = st.text_input("Enter topic for quiz (e.g. sorting, DBMS, AI)")

    if st.button("Generate Quiz"):

        if topic:
            quiz = generate_quiz(topic)

            score = 0
            answers = []

            for i, q in enumerate(quiz):
                st.markdown(f"### Q{i+1}: {q['question']}")

                choice = st.radio(
                    "Choose answer",
                    q["options"],
                    key=f"q{i}"
                )

                answers.append((choice, q["answer"]))

            if st.button("Submit Quiz"):

                score = sum([1 for a, b in answers if a == b])

                st.success(f"Your Score: {score}/5")

                # save analysis
                st.session_state.scores.append(score)
                st.session_state.attempts += 1

                st.info("Go to Student Analysis tab for performance tracking")

        else:
            st.warning("Enter a topic first")

# =========================
# TAB 3 - STUDENT ANALYSIS
# =========================
with tab3:
    st.subheader("📊 Performance Dashboard")

    if st.session_state.attempts == 0:
        st.info("No quiz attempts yet")
    else:
        avg = sum(st.session_state.scores) / len(st.session_state.scores)

        st.metric("Total Attempts", st.session_state.attempts)
        st.metric("Average Score", round(avg, 2))

        st.line_chart(st.session_state.scores)

        st.write("Score History:", st.session_state.scores)
