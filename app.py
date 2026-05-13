import streamlit as st
from transformers import pipeline
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Tutor", layout="wide")

# =========================
# LOAD MODEL (NO API KEY)
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

generator = load_model()

# =========================
# QUIZ DATA
# =========================
quiz_bank = {
    "Sorting": [
        {
            "question": "Time complexity of Merge Sort?",
            "options": ["O(n²)", "O(n log n)", "O(n)", "O(log n)"],
            "answer": "O(n log n)"
        },
        {
            "question": "Which is divide and conquer?",
            "options": ["Bubble Sort", "Merge Sort", "Stack", "Queue"],
            "answer": "Merge Sort"
        }
    ],
    "Searching": [
        {
            "question": "Binary search works on?",
            "options": ["Unsorted array", "Sorted array", "Graph", "Tree"],
            "answer": "Sorted array"
        },
        {
            "question": "Worst case of linear search?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "answer": "O(n)"
        }
    ]
}

# =========================
# AI FUNCTION
# =========================
def get_answer(question):
    prompt = f"""
You are a DAA expert tutor.

Explain clearly:
- Definition
- Steps
- Example
- Complexity

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
# UI DESIGN
# =========================
st.title("🎓 AI DAA Tutor (No API Key)")

tab1, tab2 = st.tabs(["💬 AI Chat", "📝 Quiz"])

# =========================
# CHAT SECTION
# =========================
with tab1:
    q = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if q:
            st.write(get_answer(q))
        else:
            st.warning("Enter a question first")

# =========================
# QUIZ SECTION
# =========================
with tab2:
    topic = st.selectbox("Choose Topic", list(quiz_bank.keys()))

    quiz = random.choice(quiz_bank[topic])

    st.subheader(quiz["question"])

    choice = st.radio("Options", quiz["options"])

    if st.button("Submit"):
        if choice == quiz["answer"]:
            st.success("Correct ✅")
        else:
            st.error(f"Wrong ❌ Correct answer: {quiz['answer']}")
