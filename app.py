import streamlit as st
from transformers import pipeline
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Tutor Studio", layout="wide")

# =========================
# FAST CHAT MODEL
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

model = load_model()

# =========================
# CHAT FUNCTION
# =========================
def get_answer(question):

    prompt = f"""
You are a helpful AI tutor.
Explain in simple, clear steps.

Question: {question}
Answer:
"""

    result = model(
        prompt,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"].split("Answer:")[-1].strip()

# =========================
# IMAGE GENERATION (STABLE API)
# =========================
def generate_image(prompt):

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

    headers = {
        "Authorization": "Bearer YOUR_HUGGINGFACE_TOKEN"
    }

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    return response.content

# =========================
# SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# UI HEADER
# =========================
st.title("🧠 AI Tutor Studio")
st.write("Chat with AI + Generate Images instantly")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["💬 AI Tutor", "🖼 Image Generator"])

# =========================
# 💬 CHAT SECTION
# =========================
with tab1:

    st.subheader("Ask Anything")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['text']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['text']}")

    question = st.text_input("Type your question")

    if st.button("Send"):

        if question.strip():

            st.session_state.chat_history.append({"role": "user", "text": question})

            with st.spinner("Thinking..."):
                answer = get_answer(question)

            st.session_state.chat_history.append({"role": "ai", "text": answer})

            st.rerun()

        else:
            st.warning("Please enter a question")

# =========================
# 🖼 IMAGE GENERATOR
# =========================
with tab2:

    st.subheader("Generate AI Images")

    prompt = st.text_input("Describe image (e.g. robot studying in library)")

    if st.button("Generate Image"):

        if prompt.strip():

            with st.spinner("Generating image..."):

                image_bytes = generate_image(prompt)

            st.image(image_bytes, caption=prompt)

        else:
            st.warning("Please enter a prompt")
