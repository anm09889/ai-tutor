import streamlit as st
from transformers import pipeline
import torch
import random

# ==========================
# LOAD AI MODEL (LOCAL)
# ==========================

@st.cache_resource
def load_chatbot():
    return pipeline(
        "text-generation",
        model="distilgpt2"   # lightweight fast model
    )

chatbot = load_chatbot()

# ==========================
# IMAGE MODEL (LOCAL SD)
# ==========================

from diffusers import StableDiffusionPipeline

@st.cache_resource
def load_image_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")  # Streamlit free = CPU
    return pipe

image_model = None

# ==========================
# VARIATION SYSTEM
# ==========================

def vary(text):
    styles = [
        "Explain simply:",
        "Teach step by step:",
        "Student-friendly explanation:",
        "Short clear answer:",
        "Break it down:"
    ]
    return random.choice(styles) + " " + text


# ==========================
# CHAT FUNCTION
# ==========================

def get_response(user_input):
    prompt = vary(user_input)

    result = chatbot(
        prompt,
        max_length=120,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.8
    )

    return result[0]["generated_text"]


# ==========================
# STREAMLIT UI
# ==========================

st.set_page_config(page_title="AI Tutor (No API Key)", layout="wide")

st.title("🎓 AI Tutor + Image Generator (100% FREE)")

mode = st.sidebar.selectbox("Choose Mode", ["Chat Tutor", "Image Generator"])

# ==========================
# CHAT MODE
# ==========================

if mode == "Chat Tutor":
    st.subheader("💬 Ask anything")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Enter your question")

    if st.button("Ask"):
        if user_input:
            answer = get_response(user_input)
            st.session_state.chat.append((user_input, answer))

    for q, a in reversed(st.session_state.chat):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI:** {a}")
        st.divider()

# ==========================
# IMAGE MODE
# ==========================

elif mode == "Image Generator":
    st.subheader("🎨 Generate Image (No API Key)")

    prompt = st.text_input("Describe image")

    @st.cache_resource
    def load_image_model():
        from diffusers import StableDiffusionPipeline
        import torch

        model_id = "runwayml/stable-diffusion-v1-5"

        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32
        )

        pipe = pipe.to("cpu")
        return pipe

    image_model = load_image_model()

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating image... (first time slow)"):
                image = image_model(prompt).images[0]

            st.image(image, caption=prompt)

            st.image(image, caption=prompt)
