import streamlit as st
import requests

st.set_page_config(page_title="AI Tutor", layout="wide")

st.title("🧠 AI Tutor (Fully Working)")

question = st.text_input("Ask anything")

HF_TOKEN = "YOUR_HF_TOKEN"

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_answer(prompt):

    payload = {
        "inputs": f"You are a helpful tutor. Explain simply:\n{prompt}",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # SAFE JSON HANDLING
    try:
        data = response.json()
    except:
        return f"API Error (not JSON): {response.text}"

    # HF ERROR HANDLING
    if isinstance(data, dict) and "error" in data:
        return f"HF Error: {data['error']}"

    # NORMAL OUTPUT
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
