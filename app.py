import streamlit as st
from transformers import pipeline
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Tutor Studio", layout="wide")

# =========================
# CHAT MODEL (LIGHTWEIGHT)
# =========================
@st.cache_resource
def load_chat():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

chat_model = load_chat()

# =========================
# CHAT FUNCTION
# =========================
def chat_answer(q):

    prompt = f"Explain clearly and simply:\n{q}\nAnswer:"

    result = chat_model(
        prompt,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"].split("Answer:")[-1]

# =========================
# IMAGE GENERATION (FAST API METHOD)
# =========================
def generate_image(prompt):

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    return response.content

# =========================
# SESSION
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# UI
# =========================
st.title("🧠 AI Tutor Studio")

tab1, tab2 = st.tabs(["💬 Tutor", "🖼 Image Generator"])

# =========================
# 💬 CHAT TAB
# =========================
with tab1:

    for msg in st.session_state.chat:
        st.write(msg["role"], ":", msg["text"])

    q = st.text_input("Ask anything")

    if st.button("Send"):
        if q:
            st.session_state.chat.append({"role": "You", "text": q})
            ans = chat_answer(q)
            st.session_state.chat.append({"role": "AI", "text": ans})
            st.rerun()

# =========================
# 🖼 IMAGE TAB
# =========================
with tab2:

    prompt = st.text_input("Describe image")

    if st.button("Generate Image"):

        if prompt:

            st.warning("Generating image...")

            img_bytes = generate_image(prompt)

            st.image(img_bytes)

        else:
            st.warning("Enter prompt")
