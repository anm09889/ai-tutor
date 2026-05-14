import streamlit as st
import requests

st.set_page_config(page_title="Fast AI Tutor", layout="wide")

# =========================
# UI
# =========================
st.title("🧠 Fast AI Tutor (Hugging Face API)")
st.write("Instant answers using cloud AI")

# =========================
# INPUT
# =========================
question = st.text_input("Ask anything")

# =========================
# HF API CONFIG
# =========================
HF_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =========================
# FUNCTION
# =========================
def get_answer(prompt):

    payload = {
        "inputs": f"You are a helpful tutor. Explain clearly:\n{prompt}",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    # safety fallback
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    if "error" in result:
        return "Error: " + result["error"]

    return str(result)

# =========================
# BUTTON
# =========================
if st.button("Get Answer"):

    if question.strip():

        with st.spinner("Thinking instantly..."):
            answer = get_answer(question)

        st.success("Answer:")
        st.write(answer)

    else:
        st.warning("Enter a question")
