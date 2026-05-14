import streamlit as st
import requests

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("🧠 AI Tutor (Stable Working Version)")

question = st.text_input("Ask anything")

HF_TOKEN = "YOUR_HF_TOKEN"

# ✅ ONLY STABLE MODEL FOR FREE INFERENCE
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_answer(prompt):

    payload = {
        "inputs": f"Answer clearly and simply: {prompt}"
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # SAFE JSON PARSE
    try:
        data = response.json()
    except:
        return f"API Error: {response.text}"

    # ERROR HANDLING
    if isinstance(data, dict) and "error" in data:
        return f"HF Error: {data['error']}"

    # OUTPUT HANDLING
    if isinstance(data, list):
        return data[0].get("generated_text", str(data))

    return str(data)

if st.button("Get Answer"):

    if question.strip():

        with st.spinner("Thinking..."):
            answer = get_answer(question)

        st.success("Answer:")
        st.write(answer)

    else:
        st.warning("Enter a question")
