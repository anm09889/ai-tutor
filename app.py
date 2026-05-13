import streamlit as st
import pyttsx3
import speech_recognition as sr
import random
from transformers import pipeline

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Jarvis AI Tutor",
    page_icon="🎤",
    layout="wide"
)

# =========================
# LOAD AI MODEL
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

ai = load_model()

# =========================
# VOICE ENGINE
# =========================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return "Could not understand audio"

# =========================
# AI BRAIN
# =========================
def ai_answer(topic, mode):

    prompt = f"""
Explain {topic} for college students.

Mode: {mode}

Include:
- Definition
- Working
- Real-world use
- Interview importance
- Exam notes
"""

    result = ai(prompt, max_length=200, do_sample=True)[0]["generated_text"]
    return result

# =========================
# QUIZ ENGINE
# =========================
def generate_quiz(topic):

    return [
        {
            "q": f"What is {topic} mainly used for?",
            "options": ["Problem solving", "Painting", "Music", "Graphics"],
            "ans": "Problem solving"
        },
        {
            "q": f"{topic} belongs to which field?",
            "options": ["Computer Science", "Biology", "History", "Art"],
            "ans": "Computer Science"
        },
        {
            "q": f"Key idea behind {topic}?",
            "options": ["Efficiency", "Decoration", "Noise", "Randomness"],
            "ans": "Efficiency"
        },
        {
            "q": f"{topic} improves?",
            "options": ["Performance", "Color", "Sound", "Image"],
            "ans": "Performance"
        },
        {
            "q": f"{topic} is related to?",
            "options": ["Algorithms", "Painting", "Music", "Dance"],
            "ans": "Algorithms"
        }
    ]

# =========================
# SESSION STATE
# =========================
for key in ["score", "q_index", "quiz", "started", "history", "last_topic"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "history" else 0 if key in ["score","q_index"] else False if key=="started" else ""

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align:center; color:#4F8BF9;'>🎤 JARVIS AI TUTOR</h1>
<p style='text-align:center; color:gray;'>Voice AI • Exam Mode • Smart Tutor • College Assistant</p>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🎤 Voice Tutor", "📝 Exam Mode", "🧠 Chat Mode"]
)

# =========================
# 🎤 VOICE TUTOR (CORE)
# =========================
if menu == "🎤 Voice Tutor":

    st.subheader("Jarvis Voice Assistant")

    mode = st.selectbox("Mode", ["Beginner", "Intermediate", "Advanced", "Interview"])

    col1, col2 = st.columns(2)

    with col1:

        topic = st.text_input("Enter topic")

        if st.button("Get AI Answer") and topic:
            answer = ai_answer(topic, mode)
            st.success(answer)

            if st.button("🔊 Speak Answer"):
                speak(answer)

            st.session_state.last_topic = topic
            st.session_state.history.append(topic)

    with col2:

        if st.button("🎤 Speak Question"):

            spoken = listen()
            st.write("You said:", spoken)

            answer = ai_answer(spoken, mode)

            st.success(answer)
            speak(answer)

            st.session_state.history.append(spoken)

# =========================
# 📝 EXAM MODE
# =========================
elif menu == "📝 Exam Mode":

    st.subheader("AI Exam System")

    topic = st.text_input("Enter topic")

    if st.button("Start Exam") and topic:
        st.session_state.quiz = generate_quiz(topic)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.started = True

    if st.session_state.started:

        i = st.session_state.q_index
        quiz = st.session_state.quiz

        if i < len(quiz):

            q = quiz[i]

            st.markdown(f"### Q{i+1}: {q['q']}")

            ans = st.radio("Choose answer", q["options"], key=f"q_{i}")

            if st.button("Next"):

                if ans == q["ans"]:
                    st.session_state.score += 1

                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"🎯 Score: {st.session_state.score}/5")

            if st.button("Restart"):
                st.session_state.started = False
                st.rerun()

# =========================
# 🧠 CHAT MODE (MEMORY STYLE)
# =========================
elif menu == "🧠 Chat Mode":

    st.subheader("Jarvis Chat Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Talk to Jarvis")

    if st.button("Send") and user_input:

        response = ai_answer(user_input, "Chat Mode")

        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Jarvis", response))

        speak(response)

    for role, msg in st.session_state.chat[-10:]:
        st.write(f"**{role}:** {msg}")
