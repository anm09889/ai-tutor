import streamlit as st
from transformers import pipeline

# ==========================
# LOAD LIGHTWEIGHT CHAT MODEL
# ==========================

@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )

chatbot = load_model()

# ==========================
# RESPONSE ENGINE
# ==========================

def get_answer(question):
    prompt = f"""
You are an expert AI tutor for college students.
Explain in simple steps with examples.

Question: {question}

Answer:
"""

    result = chatbot(
        prompt,
        max_new_tokens=180,
        temperature=0.7,
        do_sample=True
    )

    return result[0]["generated_text"].split("Answer:")[-1].strip()

# ==========================
# STREAMLIT UI
# ==========================

st.set_page_config(page_title="AI Tutor (Stable Version)", layout="wide")

st.title("🎓 AI Tutor (Stable No-API Version)")

if "chat" not in st.session_state:
    st.session_state.chat = []

mode = st.sidebar.selectbox("Mode", ["Chat Tutor", "Image Generator (Simple)"])

# ==========================
# CHAT MODE
# ==========================

if mode == "Chat Tutor":
    st.subheader("💬 Ask Your Question")

    user_input = st.text_input("Enter question")

    if st.button("Ask"):
        if user_input:
            answer = get_answer(user_input)
            st.session_state.chat.append((user_input, answer))

    for q, a in reversed(st.session_state.chat):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 AI:** {a}")
        st.divider()

# ==========================
# IMAGE MODE (SAFE VERSION)
# ==========================

elif mode == "Image Generator (Simple)":
    st.subheader("🎨 Image Generator (Stable Version)")

    st.warning("⚠️ Full AI image models are too heavy for free Streamlit. This uses placeholder generation.")

    prompt = st.text_input("Describe image")

    if st.button("Generate"):
        if prompt:
            st.image(
                "https://source.unsplash.com/800x500/?" + prompt,
                caption=prompt
            )
