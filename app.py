import streamlit as st
from transformers import pipeline

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Chat Tutor", layout="wide")

# =========================
# LOAD MODEL (FAST + SMALL)
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

generator = load_model()

# =========================
# CHAT MEMORY
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# UI HEADER
# =========================
st.title("🧠 AI Tutor Chat")
st.write("Ask anything — get intelligent explanations like ChatGPT")

# =========================
# CHAT DISPLAY UI
# =========================
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['text']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['text']}")

st.markdown("---")

# =========================
# INPUT
# =========================
user_input = st.text_input("Type your question")

# =========================
# GENERATE RESPONSE
# =========================
def get_response(prompt):

    full_prompt = f"""
You are a helpful AI tutor.
Explain clearly in simple steps.

Question: {prompt}
Answer:
"""

    result = generator(
        full_prompt,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"].split("Answer:")[-1].strip()

# =========================
# SEND BUTTON
# =========================
if st.button("Send"):

    if user_input:

        st.session_state.chat.append({"role": "user", "text": user_input})

        with st.spinner("Thinking..."):
            response = get_response(user_input)

        st.session_state.chat.append({"role": "ai", "text": response})

        st.rerun()
