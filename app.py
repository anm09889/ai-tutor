import streamlit as st
import random
import time
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
# UI STYLE
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #4F8BF9;
}

.card {
    background: #111827;
    padding: 18px;
    border-radius: 15px;
    color: white;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 AI Tutor Pro Max</div>', unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key in ["score", "q_index", "quiz", "started", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key == "score" or key == "q_index" else [] if key == "history" else False if key == "started" else []

# =========================
# AI TUTOR (IMPROVED)
# =========================
def ai_tutor(question, level="Beginner"):

    return f"""
📘 QUESTION: {question}

🧠 Level: {level}

✔ Explanation:
This is a core Computer Science concept used in problem solving.

✔ Real-world Use:
Search engines, AI systems, databases, apps.

✔ Key Idea:
Understand logic + structure.

✔ Tip:
Practice examples instead of memorizing.
"""

# =========================
# QUIZ GENERATOR (FIXED + BETTER)
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
            "options": ["AI", "Cooking", "Sports", "Music"],
            "ans": "AI"
        },
        {
            "q": f"Why is {topic} important?",
            "options": ["Efficiency", "Decoration", "Noise", "Color"],
            "ans": "Efficiency"
        },
        {
            "q": f"{topic} belongs to?",
            "options": ["Computer Science", "Biology", "Physics", "Art"],
            "ans": "Computer Science"
        },
        {
            "q": f"Main purpose of {topic}?",
            "options": ["Problem Solving", "Painting", "Gaming", "Cooking"],
            "ans": "Problem Solving"
        }
    ]

# =========================
# YOUTUBE HELPERS
# =========================
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

def summarize(text):
    words = text.lower().split()
    freq = Counter(words)

    sentences = text.split(".")
    scored = []

    for s in sentences:
        score = sum(freq[w] for w in s.lower().split() if w in freq)
        scored.append((score, s))

    scored.sort(reverse=True)
    return ". ".join([s for _, s in scored[:5]])

# =========================
# IMAGES
# =========================
def get_images(topic):
    return [
        f"https://source.unsplash.com/800x400/?{topic}",
        f"https://source.unsplash.com/800x400/?{topic},technology",
        f"https://source.unsplash.com/800x400/?{topic},computer"
    ]

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🤖 AI Tutor", "📝 Quiz", "🎥 YouTube Learning", "📊 Insights"]
)

# =========================
# 🤖 AI TUTOR
# =========================
if menu == "🤖 AI Tutor":

    st.subheader("Ask Anything")

    q = st.text_input("Enter question")
    level = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Get Answer"):
        if q:
            st.success(ai_tutor(q, level))
            st.session_state.history.append(q)

    st.write("Recent Questions:")
    st.write(st.session_state.history[-5:])

# =========================
# 📝 QUIZ (FULL FIXED)
# =========================
elif menu == "📝 Quiz":

    st.subheader("Smart Quiz Engine")

    topic = st.text_input("Enter topic")

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

            # FIX: unique key per question
            key = f"q_{i}"

            answer = st.radio(
                "Choose answer",
                qdata["options"],
                key=key
            )

            if st.button("Next"):

                if answer == qdata["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"Final Score: {st.session_state.score}/5")

            if st.button("Restart"):
                st.session_state.started = False
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.rerun()

# =========================
# 🎥 YOUTUBE LEARNING (UPGRADED)
# =========================
elif menu == "🎥 YouTube Learning":

    st.subheader("YouTube AI Learning System")

    url = st.text_input("Paste YouTube URL")

    topic = st.text_input("Topic for visualization")

    if st.button("Generate Learning"):

        if url:

            try:
                vid = get_video_id(url)
                transcript = fetch_transcript(vid)

                st.markdown("### 📄 AI Summary")
                st.info(summarize(transcript))

                st.markdown("### 🧠 Key Learning Points")
                st.write([
                    "Understand concept flow",
                    "Focus on real-world usage",
                    "Practice with examples"
                ])

                st.markdown("### 🖼️ Visual Learning")
                for img in get_images(topic):
                    st.image(img)

                st.markdown("### 🔁 Flowchart")

                dot = graphviz.Digraph()
                dot.node("A", topic)
                dot.node("B", "Definition")
                dot.node("C", "Working")
                dot.node("D", "Applications")

                dot.edges(["AB", "AC", "AD"])

                st.graphviz_chart(dot)

            except:
                st.error("Transcript not available for this video.")

# =========================
# 📊 INSIGHTS DASHBOARD
# =========================
elif menu == "📊 Insights":

    st.subheader("Learning Analytics")

    st.metric("Quiz Score", st.session_state.score)
    st.metric("Questions Asked", len(st.session_state.history))

    st.progress(min(st.session_state.q_index / 5, 1.0))

    st.write("Recent Activity")
    st.write(st.session_state.history[-10:])
