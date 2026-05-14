import streamlit as st
import requests

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("🧠 AI Tutor (Fixed API)")

question = st.text_input("Ask anything")

HF_TOKEN = "YOUR_HF_TOKEN"

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_answer(prompt):

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🔥 SAFE HANDLING
    try:
        data = response.json()
    except:
        return f"API Error (not JSON): {response.text}"

    # If error returned by HF
    if isinstance(data, dict) and "error" in data:
        return f"HF Error: {data['error']}"

    # Blenderbot response format
    if isinstance(data, list):
        return data[0].get("generated_text", str(data))

    return str(data)

if st.button("Get Answer"):
    if question:
        with st.spinner("Thinking..."):
            answer = get_answer(question)

        st.success("Answer:")
        st.write(answer)
    else:
        st.warning("Enter a question")
