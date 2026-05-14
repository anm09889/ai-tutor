import streamlit as st
import random

# ==========================
# SMART TUTOR ENGINE (NO ML)
# ==========================

def tutor_response(question):
    question = question.lower()

    if "data structure" in question:
        return "A Data Structure is a way to organize data efficiently. Example: arrays, linked lists, trees. Arrays store elements in continuous memory."

    elif "algorithm" in question:
        return "An algorithm is a step-by-step procedure to solve a problem. Example: sorting algorithms like Bubble Sort or Merge Sort."

    elif "dbms" in question:
        return "DBMS (Database Management System) manages databases. It allows storing, retrieving, and managing data efficiently."

    elif "os" in question or "operating system" in question:
        return "An Operating System manages hardware and software resources. Example: Windows, Linux."

    else:
        replies = [
            "Let me explain simply: this topic is important in computer science. Break it into smaller parts and study step by step.",
            "Good question! Think of it as a concept used in real-world systems. Try understanding definition + example.",
            "Here is a simple explanation: focus on basics first, then move to advanced details."
        ]
        return random.choice(replies)

# ==========================
# IMAGE GENERATION (SAFE)
# ==========================

def generate_image(prompt):
    return f"https://source.unsplash.com/800x500/?{prompt}"

# ==========================
# STREAMLIT UI
# ==========================

st.set_page_config(page_title="AI Tutor Stable", layout="wide")

st.title("🎓 AI Tutor (Stable No-API Version)")

mode = st.sidebar.selectbox("Choose Mode", ["Chat Tutor", "Image Generator"])

# ==========================
# CHAT MODE
# ==========================

if mode == "Chat Tutor":
    st.subheader("💬 Ask Your Question")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Enter your question")

    if st.button("Ask"):
        if user_input:
            answer = tutor_response(user_input)
            st.session_state.chat.append((user_input, answer))

    for q, a in reversed(st.session_state.chat):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI Tutor:** {a}")
        st.divider()

# ==========================
# IMAGE MODE
# ==========================

elif mode == "Image Generator":
    st.subheader("🎨 Image Generator (No API)")

    prompt = st.text_input("Describe image")

    if st.button("Generate"):
        if prompt:
            img_url = generate_image(prompt)
            st.image(img_url, caption=prompt)
