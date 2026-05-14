import streamlit as st
import sqlite3
import hashlib
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Tutor Login System", page_icon="🎓", layout="wide")

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS scores (
    username TEXT,
    score INTEGER
)
""")
conn.commit()

# =========================
# PASSWORD HASH
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# AUTH FUNCTIONS
# =========================
def signup_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# LOGIN / SIGNUP PAGE
# =========================
if st.session_state.user is None:

    st.title("🎓 AI Tutor Login System")

    menu = st.radio("Choose option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if signup_user(username, password):
                st.success("Account created! Now login.")
            else:
                st.error("User already exists")

    if menu == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# =========================
# MAIN APP (AFTER LOGIN)
# =========================
else:

    st.sidebar.success(f"Logged in as {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    menu = st.sidebar.radio("Menu", ["AI Tutor", "Quiz", "Analysis"])

    # =========================
    # AI TUTOR
    # =========================
    if menu == "AI Tutor":
        st.title("🤖 AI Tutor")

        q = st.text_input("Ask question")

        if st.button("Get Answer"):
            st.success(f"Answer for: {q}")

    # =========================
    # QUIZ
    # =========================
    elif menu == "Quiz":

        st.title("📝 Quiz System")

        topic = st.text_input("Enter topic")

        def generate_quiz(topic):
            return [
                {"q": f"What is {topic}?", "ans": "Concept"},
                {"q": f"Where is {topic} used?", "ans": "CS"},
                {"q": f"Explain {topic}", "ans": "Theory"},
                {"q": f"Importance of {topic}", "ans": "High"},
                {"q": f"{topic} belongs to?", "ans": "DSA"}
            ]

        if "quiz" not in st.session_state:
            st.session_state.quiz = []
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.started = False

        if st.button("Start Quiz"):
            if topic:
                st.session_state.quiz = generate_quiz(topic)
                st.session_state.index = 0
                st.session_state.score = 0
                st.session_state.started = True

        if st.session_state.started:

            qz = st.session_state.quiz
            i = st.session_state.index

            if i < len(qz):

                st.subheader(qz[i]["q"])
                ans = st.radio("Answer", ["Concept", "CS", "Theory", "High", "DSA"], key=i)

                if st.button("Next"):
                    if ans == qz[i]["ans"]:
                        st.session_state.score += 1
                    st.session_state.index += 1
                    st.rerun()

            else:
                st.success(f"Score: {st.session_state.score}/5")

                c.execute("INSERT INTO scores VALUES (?, ?)",
                          (st.session_state.user, st.session_state.score))
                conn.commit()

                st.session_state.started = False

    # =========================
    # ANALYSIS
    # =========================
    elif menu == "Analysis":

        st.title("📊 Student Analysis")

        c.execute("SELECT score FROM scores WHERE username=?",
                  (st.session_state.user,))
        data = c.fetchall()

        if not data:
            st.info("No data yet")
        else:
            scores = [i[0] for i in data]

            st.metric("Total Attempts", len(scores))
            st.metric("Average Score", sum(scores)/len(scores))

            st.line_chart(scores)
