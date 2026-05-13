import streamlit as st
from transformers import pipeline
import random
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

.quiz-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1f26;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("🎓 AI Personal Tutor Pro")
st.caption("AI Tutor + Smart Quiz + Student Analysis")

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():

    generator = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )

    return generator

generator = load_model()

# ==========================================
# SESSION VARIABLES
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "results" not in st.session_state:
    st.session_state.results = []

# ==========================================
# QUIZ DATABASE
# ==========================================

quiz_data = {

    "Sorting": [

        {
            "question": "What is the average complexity of Quick Sort?",

            "options": [
                "O(n)",
                "O(log n)",
                "O(n log n)",
                "O(n²)"
            ],

            "answer": "O(n log n)",

            "explanation": """
Quick Sort divides the array recursively.
Average complexity becomes O(n log n).
""",

            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif"
        },

        {
            "question": "Which sorting algorithm uses Divide and Conquer?",

            "options": [
                "Bubble Sort",
                "Merge Sort",
                "Linear Search",
                "DFS"
            ],

            "answer": "Merge Sort",

            "explanation": """
Merge Sort recursively divides the array
and merges sorted parts together.
""",

            "image": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif"
        }
    ],

    "Graphs": [

        {
            "question": "Which data structure is used in BFS?",

            "options": [
                "Stack",
                "Queue",
                "Heap",
                "Tree"
            ],

            "answer": "Queue",

            "explanation": """
BFS explores nodes level by level,
so Queue is used.
""",

            "image": "https://upload.wikimedia.org/wikipedia/commons/4/46/Animated_BFS.gif"
        },

        {
            "question": "DFS mainly uses?",

            "options": [
                "Queue",
                "Stack",
                "Heap",
                "Array"
            ],

            "answer": "Stack",

            "explanation": """
DFS goes deep first,
so Stack is used internally.
""",

            "image": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Depth-First-Search.gif"
        }
    ]
}

# ==========================================
# SIDEBAR
# ==========================================

page = st.sidebar.radio(
    "Choose Section",
    [
        "🤖 AI Tutor",
        "📝 Smart Quiz",
        "📊 Student Analysis"
    ]
)

# ==========================================
# AI TUTOR PAGE
# ==========================================

if page == "🤖 AI Tutor":

    st.header("🤖 AI Tutor")

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask any question...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    words = len(prompt.split())

                    if words < 5:
                        max_tokens = 80

                    elif words < 15:
                        max_tokens = 150

                    else:
                        max_tokens = 250

                    system_prompt = f"""
You are an expert educational AI tutor.

Rules:
- Explain clearly
- No random text
- No repeated lines
- Give educational answers only

Question:
{prompt}

Answer:
"""

                    result = generator(
                        system_prompt,
                        max_new_tokens=max_tokens,
                        do_sample=False,
                        temperature=0.1,
                        repetition_penalty=1.2,
                        no_repeat_ngram_size=3,
                        truncation=True,
                        pad_token_id=generator.tokenizer.eos_token_id
                    )

                    text = result[0]["generated_text"]

                    answer = text.replace(system_prompt, "").strip()

                    st.markdown(answer)

                except Exception as e:

                    answer = f"❌ Error: {e}"

                    st.error(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

# ==========================================
# QUIZ PAGE
# ==========================================

elif page == "📝 Smart Quiz":

    st.header("📝 Smart Quiz System")

    topic = st.selectbox(
        "Select Quiz Topic",
        list(quiz_data.keys())
    )

    questions = quiz_data[topic]

    if st.button("🚀 Start Quiz"):

        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.results = []

    if st.session_state.quiz_started:

        index = st.session_state.current_question

        if index < len(questions):

            q = questions[index]

            st.subheader(f"Question {index + 1}")

            st.image(q["image"], width=500)

            st.markdown(f"### {q['question']}")

            selected = st.radio(
                "Choose Answer",
                q["options"],
                key=f"quiz_{index}"
            )

            if st.button("Submit Answer"):

                correct = selected == q["answer"]

                if correct:

                    st.success("✅ Correct Answer")
                    st.session_state.score += 1

                else:

                    st.error("❌ Wrong Answer")

                st.info(f"✔ Correct Answer: {q['answer']}")

                st.write(q["explanation"])

                st.session_state.results.append({

                    "Question": q["question"],
                    "Your Answer": selected,
                    "Correct Answer": q["answer"],
                    "Result": "Correct" if correct else "Wrong"
                })

                st.session_state.current_question += 1

                st.rerun()

        else:

            st.success("🎉 Quiz Completed")

            score = st.session_state.score
            total = len(questions)

            percentage = (score / total) * 100

            st.metric("Final Score", f"{score}/{total}")

            st.progress(int(percentage))

            st.write(f"### Percentage: {percentage:.2f}%")

            if percentage >= 80:

                st.success("Excellent Performance 🎉")

            elif percentage >= 50:

                st.warning("Good Performance 👍")

            else:

                st.error("Needs Improvement 📚")

# ==========================================
# STUDENT ANALYSIS PAGE
# ==========================================

elif page == "📊 Student Analysis":

    st.header("📊 Full Student Analysis")

    if len(st.session_state.results) == 0:

        st.warning("No quiz data available.")

    else:

        df = pd.DataFrame(st.session_state.results)

        st.dataframe(df)

        total = len(df)

        correct = len(df[df["Result"] == "Correct"])

        wrong = total - correct

        accuracy = (correct / total) * 100

        st.subheader("📈 Performance Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Questions", total)

        col2.metric("Correct Answers", correct)

        col3.metric("Accuracy", f"{accuracy:.2f}%")

        st.subheader("📉 Result Distribution")

        chart_data = pd.DataFrame({
            "Category": ["Correct", "Wrong"],
            "Count": [correct, wrong]
        })

        st.bar_chart(chart_data.set_index("Category"))

        st.subheader("🧠 AI Performance Review")

        if accuracy >= 80:

            st.success("""
Excellent understanding of concepts.

Strengths:
- Strong problem solving
- Good conceptual clarity
- High accuracy
""")

        elif accuracy >= 50:

            st.warning("""
Average performance.

Suggestions:
- Practice more MCQs
- Revise weak topics
- Improve speed and accuracy
""")

        else:

            st.error("""
Needs significant improvement.

Recommendations:
- Study fundamentals again
- Solve practice questions daily
- Focus on weak areas
""")

# ==========================================
# FOOTER
# ==========================================

st.sidebar.divider()

st.sidebar.write("🎓 AI Tutor Pro")
st.sidebar.write("Built using Streamlit + Hugging Face")