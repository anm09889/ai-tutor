import streamlit as st
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Tutor + Image Generator", layout="wide")

# =========================
# LOAD TEXT AI (FAST)
# =========================
@st.cache_resource
def load_chat_model():
    return pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

chat_model = load_chat_model()

# =========================
# LOAD IMAGE MODEL (LIGHT VERSION)
# =========================
@st.cache_resource
def load_image_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

image_model = load_image_model()

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# AI CHAT FUNCTION
# =========================
def get_chat_response(prompt):

    full_prompt = f"""
You are a helpful AI tutor. Explain clearly and simply.

Question: {prompt}
Answer:
"""

    result = chat_model(
        full_prompt,
        max_new_tokens=180,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"].split("Answer:")[-1].strip()

# =========================
# IMAGE GENERATION FUNCTION
# =========================
def generate_image(prompt):

    image = image_model(prompt).images[0]
    return image

# =========================
# UI HEADER
# =========================
st.title("🧠 AI Learning Studio")
st.write("Chat with AI + Generate Images from text")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["💬 AI Tutor", "🖼 Image Generator"])

# =========================
# 💬 CHAT TAB
# =========================
with tab1:

    st.subheader("AI Tutor Chat")

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['text']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['text']}")

    user_input = st.text_input("Ask a question")

    if st.button("Send"):

        if user_input:

            st.session_state.chat.append({"role": "user", "text": user_input})

            with st.spinner("Thinking..."):
                response = get_chat_response(user_input)

            st.session_state.chat.append({"role": "ai", "text": response})

            st.rerun()

# =========================
# 🖼 IMAGE TAB
# =========================
with tab2:

    st.subheader("AI Image Generator")

    prompt = st.text_input("Describe image (e.g. 'robot studying in library')")

    if st.button("Generate Image"):

        if prompt:

            with st.spinner("Generating image... (may take 10–30 sec)"):

                img = generate_image(prompt)

            st.image(img, caption=prompt)

        else:
            st.warning("Enter an image description")
