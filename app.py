# ==========================================
# 🎓 AI PERSONAL DAA TUTOR (STABLE VERSION)
# ==========================================

!pip install -q gradio transformers sentencepiece torch

import gradio as gr
from transformers import pipeline

# ==========================================
# LOAD MODEL (SAFE + STABLE)
# ==========================================

print("⏳ Loading AI Tutor Model...")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"   # ✅ SAFE MODEL (no crash)
)

print("✅ Model Loaded!")

# ==========================================
# RESPONSE FUNCTION
# ==========================================

def answer_question(question):

    prompt = f"""
You are a DAA (Design and Analysis of Algorithms) tutor.

Explain in simple college level:

Topic: {question}

Format:
1. Definition
2. Working steps
3. Example
4. Time Complexity (Big-O)
5. Advantages
6. Disadvantages

Keep it short, correct, and structured.
"""

    output = generator(
        prompt,
        max_new_tokens=180,
        do_sample=False
    )

    return output[0]["generated_text"]

# ==========================================
# CHAT FUNCTION (FIXED)
# ==========================================

def chat(user_input, history):
    if history is None:
        history = []

    response = answer_question(user_input)

    history.append((user_input, response))

    return history, history

# ==========================================
# UI
# ==========================================

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🎓 AI DAA Tutor (Stable Version)")

    chatbot = gr.Chatbot(height=450)

    state = gr.State([])

    msg = gr.Textbox(
        placeholder="Ask: Explain Merge Sort / Quick Sort / DP",
        label="Your Question"
    )

    btn = gr.Button("Ask AI 🚀")
    clear = gr.Button("Clear 🗑")

    btn.click(chat, inputs=[msg, state], outputs=[chatbot, state])
    msg.submit(chat, inputs=[msg, state], outputs=[chatbot, state])

    clear.click(lambda: ([], []), outputs=[chatbot, state])

demo.launch()
