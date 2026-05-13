import streamlit as st
import random
import time
import requests
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi
import graphviz

# =========================
# PAGE CONFIG (MODERN UI)
# =========================
st.set_page_config(
    page_title="AI Tutor Pro",
    page_icon="🎓",
    layout="wide"
)

# =========================
# MODERN UI STYLE
# =========================
st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        color: #4F8BF9;
    }

    .sub-text {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 20px;
    }

    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">🎓 AI Tutor Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Smart Learning • Quiz • YouTube AI Summary • Visual Learning</div>', unsafe_allow_html=True)

# =========================
# SIMPLE AI TUTOR
# =========================
def ai_tutor(question):
    return f"""
📘 ANSWER:
{question}

✔ Definition:
A core Computer Science concept.

✔ Explanation:
Used in solving structured problems efficiently.

✔ Example:
Used in algorithms, databases, AI systems.

✔ Key Idea:
Focus on logic and optimization.
"""

# =========================
# QUIZ SYSTEM (FIXED)
# =========================
def generate_quiz(topic):
    return [
        {
            "q": f"What is {topic}?",
            "options": ["Concept", "Algorithm", "Data", "System"],
            "ans": "Concept"
        },
        {
            "q": f"Where is {topic} used?",
            "options": ["Web", "Algorithms", "Music", "Games"],
            "ans": "Algorithms"
        },
        {
            "q": f"Why is {topic} important?",
            "options": ["Efficiency", "Style", "Speed", "Color"],
            "ans": "Efficiency"
        },
        {
            "q": f"{topic} belongs to which field?",
            "options": ["CS", "Biology", "Physics", "Art"],
            "ans": "CS"
        },
        {
            "q": f"Main purpose of {topic}?",
            "options": ["Problem Solving", "Painting", "Cooking", "Sports"],
            "ans": "Problem Solving"
        }
    ]

# =========================
# YOUTUBE HELPERS (FIXED)
# =========================
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

def summarize_text(text):
    words = text.lower().split()
    freq = Counter(words)

    sentences = text.split(".")
    scored = []

    for s in sentences:
        score = sum(freq[w] for w in s.lower().split() if w in freq)
        scored.append((score, s))

    scored.sort(reverse=True)
    return ". ".join([s for _, s in scored[:4]])

# =========================
# IMAGES
# =========================
def get_images(topic):
    return [
        f"https://source.unsplash.com/800x400/?{topic}",
        f"https://source.unsplash.com/800x400/?{topic},computer",
        f"https://source.unsplash.com/800x400/?{topic},technology"
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

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Quiz", "🎥 YouTube Learning", "📊 Dashboard"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("Ask Anything")

    q = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if q:
            st.success(ai_tutor(q))

# =========================
# 📝 QUIZ (FIXED OPTIONS)
# =========================
elif menu == "📝 Quiz":

    st.subheader("Smart Quiz System")

    topic = st.text_input("Enter topic")

    if st.button("Start Quiz"):
        if topic:
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

            answer = st.radio("Choose answer", qdata["options"], key=i)

            if st.button("Next Question"):

                if answer == qdata["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"Final Score: {st.session_state.score}/5")

            if st.button("Restart Quiz"):
                st.session_state.started = False
                st.rerun()

# =========================
# 🎥 YOUTUBE (FIXED SINGLE INPUT)
# =========================
elif menu == "🎥 YouTube Learning":

    st.subheader("YouTube AI Learning Hub")

    url = st.text_input("Paste YouTube URL here")

    topic = st.text_input("Topic for visuals")

    if st.button("Generate Learning Content"):

        if url:

            video_id = get_video_id(url)

            try:
                transcript = fetch_transcript(video_id)
                summary = summarize_text(transcript)

                st.markdown("### 📄 AI Summary")
                st.info(summary)

                st.markdown("### 🖼️ Visual Learning")
                for img in get_images(topic):
                    st.image(img)

                st.markdown("### 🔁 Flowchart")

                dot = graphviz.Digraph()
                dot.node("A", topic)
                dot.node("B", "Definition")
                dot.node("C", "Working")
                dot.node("D", "Use Cases")

                dot.edges(["AB", "AC", "AD"])

                st.graphviz_chart(dot)

            except:
                st.error("Transcript not available for this video.")

# =========================
# 📊 DASHBOARD
# =========================
elif menu == "📊 Dashboard":

    st.subheader("Student Analytics")

    st.metric("Quiz Score", st.session_state.score)
    st.metric("Quiz Progress", f"{st.session_state.q_index}/5")

    st.progress(st.session_state.q_index / 5 if st.session_state.started else 0)
