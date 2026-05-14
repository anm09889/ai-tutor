# ==========================================
# 🎓 AI PERSONAL DAA TUTOR (FIXED VERSION)
# ==========================================

# INSTALL LIBRARIES
!pip install -q gradio transformers accelerate sentencepiece torch

# ==========================================
# IMPORT LIBRARIES
# ==========================================

import gradio as gr
from transformers import pipeline

# ==========================================
# LOAD BETTER HUGGING FACE MODEL
# ==========================================

print("⏳ Loading AI Tutor Model...")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-large"   # ✅ FIXED (better accuracy)
)

print("✅ AI Tutor Loaded Successfully!")

# ==========================================
# AI ANSWER FUNCTION (FIXED PROMPT)
# ==========================================

def answer_question(question):

    prompt = f"""
You are a strict expert tutor for Design and Analysis of Algorithms (DAA).

Topic: {question}

Answer in this format only:

1. Definition (short and clear)
2. Working / Algorithm (stepwise points)
3. Example (simple)
4. Time Complexity (Big-O notation)
5. Advantages (3 points)
6. Disadvantages (3 points)

Rules:
- Do NOT include unnecessary text
- Do NOT hallucinate or add wrong facts
- Keep answers exam-ready and simple
"""

    try:
        result = generator(
            prompt,
            max_new_tokens=180,   # ✅ controlled output
            do_sample=False,      # ✅ no randomness
            num_beams=4           # ✅ better accuracy
        )

        return result[0]["generated_text"]

    except Exception as e:
        return f"❌ Error: {e}"

# ==========================================
# CHATBOT FUNCTION
# ==========================================

def chatbot_response(message, history):

    response = answer_question(message)
    history.append((message, response))

    return history, history

# ==========================================
# UI STYLING
# ==========================================

custom_css = """
body {
    background-color: #0f172a;
    color: white;
}
.gradio-container {
    font-family: Arial;
}
"""

# ==========================================
# GRADIO UI
# ==========================================

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🎓 AI Personal Tutor for DAA
    ### Ask any topic like Merge Sort, Quick Sort, DP, Greedy, etc.
    """)

    chatbot = gr.Chatbot(height=500)

    state = gr.State([])

    msg = gr.Textbox(
        placeholder="Example: Explain Merge Sort",
        label="Ask Your Question"
    )

    send_btn = gr.Button("🚀 Ask AI Tutor", variant="primary")
    clear_btn = gr.Button("🗑 Clear Chat")

    # SEND
    send_btn.click(
        chatbot_response,
        inputs=[msg, state],
        outputs=[chatbot, state]
    )

    msg.submit(
        chatbot_response,
        inputs=[msg, state],
        outputs=[chatbot, state]
    )

    # CLEAR
    clear_btn.click(
        lambda: ([], []),
        outputs=[chatbot, state]
    )

# ==========================================
# LAUNCH APP
# ==========================================

demo.launch(debug=True)
