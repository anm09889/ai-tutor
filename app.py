import streamlit as st
import random
import time
import requests
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi
import graphviz

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SIMPLE AI TUTOR
# =========================
def ai_tutor(question):
    return f"""
📘 ANSWER:

{question}

✔ Definition:
This is an important Computer Science concept.

✔ Explanation:
It helps in structured problem solving and optimization.

✔ Example:
Used in algorithms, AI systems, and real-world applications.

✔ Key Idea:
Understand logic, not memorization.

✔ Tip:
Practice with examples for mastery.
"""

# =========================
# QUIZ GENERATOR
# =========================
def generate_quiz(topic):
    return [
        (f"What is {topic}?", "Concept"),
        (f"Where is {topic} used?", "Algorithms"),
        (f"Why is {topic} important?", "Efficiency"),
        (f"Explain {topic}", "Steps"),
        (f"{topic} belongs to?", "CS")
    ]

# =========================
# YOUTUBE UTILITIES
# =========================
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t["text"] for t in transcript])
    return text

def summarize_text(text, max_sentences=5):
    words = text.lower().split()
    freq = Counter(words)

    sentences = text.split(".")
    scored = []

    for s in sentences:
        score = sum(freq[w] for w in s.lower().split() if w in freq)
        scored.append((score, s))

    scored.sort(reverse=True)
    summary = ".".join([s for _, s in scored[:max_sentences]])

    return summary

# =========================
# IMAGE FETCH (UNSPLASH)
# =========================
def get_images(topic):
    return [
        f"https://source.unsplash.com/600x400/?{topic},technology",
        f"https://source.unsplash.com/600x400/?{topic},computer",
        f"https://source.unsplash.com/600x400/?{topic},data"
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
menu = st.sidebar.radio(
    "📌 MENU",
    ["🤖 AI Tutor", "📝 Quiz", "🎥 YouTube Learning", "🧰 Tools", "📊 Analysis"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.title("🎓 AI Tutor Pro")

    question = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if question:
            answer = ai_tutor(question)
            st.success(answer)
            st.session_state.history.append(question)
        else:
            st.warning("Enter a question")

    st.subheader("📌 Recent Questions")
    st.write(st.session_state.history[-5:])

# =========================
# 📝 QUIZ
# =========================
elif menu == "📝 Quiz":

    st.title("📝 Smart Quiz System")

    topic = st.text_input("Enter topic")

    if st.button("Start Quiz"):
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

            options = ["Concept", "Algorithms", "Efficiency", "Steps", "CS"]
            answer = st.radio("Choose answer", options, key=i)

            if st.button("Next"):

                if answer == correct:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎉 Score: {st.session_state.score}/5")

            if st.button("Restart"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.rerun()

# =========================
# 🎥 YOUTUBE LEARNING HUB
# =========================
elif menu == "🎥 YouTube Learning":

    st.title("🎥 YouTube AI Learning Hub")

    url = st.text_input("Paste YouTube URL")

    topic = st.text_input("Topic for visuals (e.g. sorting, DBMS)")

    if st.button("Analyze Video"):

        if url:

            video_id = get_video_id(url)

            try:
                transcript = fetch_transcript(video_id)

                st.subheader("📄 Auto Summary")
                summary = summarize_text(transcript)
                st.write(summary)

                st.subheader("🖼️ Visual Learning Images")
                images = get_images(topic)

                for img in images:
                    st.image(img)

                st.subheader("🔁 Flowchart (Concept Map)")

                dot = graphviz.Digraph()

                dot.node("A", topic)
                dot.node("B", "Definition")
                dot.node("C", "Working")
                dot.node("D", "Applications")

                dot.edges(["AB", "AC", "AD"])

                st.graphviz_chart(dot)

                st.subheader("🧪 Simple Simulation")

                st.write("Sorting Simulation (Bubble Sort Steps)")

                data = [random.randint(1, 20) for _ in range(10)]
                st.write("Initial Data:", data)

                if st.button("Run Simulation"):

                    chart = st.line_chart(data)

                    arr = data[:]

                    for i in range(len(arr)):
                        for j in range(len(arr)-i-1):
                            if arr[j] > arr[j+1]:
                                arr[j], arr[j+1] = arr[j+1], arr[j]

                            chart.add_rows(arr)
                            time.sleep(0.2)

            except Exception as e:
                st.error("Could not fetch transcript. Try another video.")

# =========================
# 🧰 TOOLS
# =========================
elif menu == "🧰 Tools":

    st.title("🧰 Study Tools")

    tool = st.selectbox("Choose Tool", [
        "Quick Notes Maker",
        "Study Timer",
        "Simple Calculator"
    ])

    if tool == "Quick Notes Maker":
        text = st.text_area("Topic")
        if st.button("Generate"):
            st.info(f"📘 {text} is a key CS concept used in problem solving and systems.")

    elif tool == "Study Timer":
        minutes = st.number_input("Minutes", 1, 60, 5)
        if st.button("Start"):
            st.success(f"Timer started for {minutes} minutes")

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
# 📊 ANALYSIS
# =========================
elif menu == "📊 Analysis":

    st.title("📊 Student Analytics")

    st.metric("Questions Asked", len(st.session_state.history))
    st.metric("Last Quiz Score", st.session_state.score)

    st.write("Recent Activity")
    st.write(st.session_state.history[-10:])
