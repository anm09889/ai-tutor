import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# ==========================
# CHAT MODEL (BETTER LLM)
# ==========================

@st.cache_resource
def load_chat_model():
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )

chatbot = load_chat_model()

# ==========================
# IMAGE MODEL (FAST SD TURBO)
# ==========================

@st.cache_resource
def load_image_model():
    from diffusers import AutoPipelineForText2Image

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=torch.float32
    ).to("cpu")

    return pipe

image_model = load_image_model()

# ==========================
# SMART PROMPT SYSTEM
# ==========================

def build_prompt(user_input):
    return f"""
You are an expert AI tutor for college students.

Explain clearly, step-by-step, with examples if needed.

Question: {user_input}

Answer:
"""

# ==========================
# STREAMLIT UI
# ==========================

st.set_page_config(page_title="AI Tutor Pro (No API)", layout="wide")

st.title("🎓 AI Tutor Pro (No API Key, Better Model)")

mode = st.sidebar.selectbox("Mode", ["Chat Tutor", "Image Generator"])

# ==========================
# CHAT MODE
# ==========================

if mode == "Chat Tutor":
    st.subheader("💬 Ask Your Question")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Enter question")

    if st.button("Ask"):
        if user_input:
            prompt = build_prompt(user_input)

            result = chatbot(
                prompt,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True
            )

            answer = result[0]["generated_text"]

            st.session_state.chat.append((user_input, answer))

    for q, a in reversed(st.session_state.chat):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI:** {a}")
        st.divider()

# ==========================
# IMAGE MODE
# ==========================

elif mode == "Image Generator":
    st.subheader("🎨 AI Image Generator")

    prompt = st.text_input("Describe image")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating image..."):

                image = image_model(prompt=prompt).images[0]

            st.image(image, caption=prompt)
