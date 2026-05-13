import streamlit as st

st.set_page_config(page_title="AI Tutor ChatGPT Style", layout="wide")

# =========================
# SESSION STATE (CHAT MEMORY)
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SIMPLE AI RESPONSE (YOU CAN REPLACE WITH GEMINI/HF)
# =========================
def get_response(user_input):
    return f"🤖 AI Tutor: I understand '{user_input}'. Here is a simple explanation... (you can connect real AI model here)"

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio("Menu", ["💬 AI Tutor", "📝 Quiz", "📊 Analysis"])

# =========================
# 💬 CHATGPT STYLE TUTOR
# =========================
if menu == "💬 AI Tutor":

    st.title("💬 AI Tutor (ChatGPT Style)")

    # DISPLAY CHAT HISTORY
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align:right; background:#DCF8C6; padding:10px; border-radius:10px; margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align:left; background:#F1F0F0; padding:10px; border-radius:10px; margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True
            )

    user_input = st.text_input("Type your message")

    if st.button("Send"):
        if user_input:

            # save user message
            st.session_state.messages.append({"role": "user", "text": user_input})

            # get AI response
            response = get_response(user_input)

            st.session_state.messages.append({"role": "ai", "text": response})

            st.rerun()

# =========================
# 📝 QUIZ SECTION (SIMPLE)
# =========================
elif menu == "📝 Quiz":

    st.title("📝 Quiz Section")

    topic = st.text_input("Enter topic")

    if st.button("Start Quiz"):

        questions = [
            f"What is {topic}?",
            f"Explain {topic} concept",
            f"Where is {topic} used?",
            f"Advantages of {topic}?",
            f"Complexity of {topic}?"
        ]

        score = 0

        for i, q in enumerate(questions):
            st.write(q)
            ans = st.radio(f"Answer {i+1}", ["A", "B", "C", "D"], key=i)

            if ans:
                score += 1

        st.success(f"Score: {score}/5")

# =========================
# 📊 ANALYSIS SECTION
# =========================
elif menu == "📊 Analysis":

    st.title("📊 Student Analysis")

    st.info("Upgrade coming: connect quiz + AI tracking system")
