import streamlit as st
import requests

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("🧠 AI Tutor (Stable Working Version)")

question = st.text_input("Ask anything")

HF_TOKEN = "YOUR_HF_TOKEN"

# ✅ SAFE WORKING MODEL
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_answer(prompt):

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🔥 SAFE RESPONSE HANDLING
    try:
        data = response.json()
    except:
        return f"API Error: {response.text}"

    # HF error handling
    if isinstance(data, dict) and "error" in data:
        return f"HF Error: {data['error']}"

    # correct format handling
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return str(data)

if st.button("Get Answer"):
    if question.strip():
        with st.spinner("Thinking..."):
            answer = get_answer(question)

        st.success("Answer:")
        st.write(answer)
    else:
        st.warning("Enter a question")
