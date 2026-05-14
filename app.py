# ==========================================
# 🎓 FAST & ACCURATE AI DAA TUTOR (FINAL)
# ==========================================


# ==========================================
# IMPORTS
# ==========================================

from transformers import pipeline
from IPython.display import display, clear_output
import ipywidgets as widgets
import random

# ==========================================
# LOAD MODEL (OPTIMIZED)
# ==========================================

print("⏳ Loading optimized AI model...")

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

print("✅ Model Loaded!")

# ==========================================
# QUIZ BANK (same as yours)
# ==========================================

quiz_bank = [
    {
        "question": "What is the average time complexity of Quick Sort?",
        "options": ["O(n²)", "O(log n)", "O(n log n)", "O(n)"],
        "answer": "O(n log n)"
    },
    {
        "question": "Which algorithm uses Divide and Conquer approach?",
        "options": ["Merge Sort", "Linear Search", "Bubble Sort", "DFS"],
        "answer": "Merge Sort"
    },
    {
        "question": "Which data structure is mainly used in BFS?",
        "options": ["Stack", "Queue", "Heap", "Tree"],
        "answer": "Queue"
    },
    {
        "question": "What is the worst case complexity of Binary Search?",
        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
        "answer": "O(log n)"
    },
    {
        "question": "Dynamic Programming is mainly used when problems have:",
        "options": [
            "Overlapping subproblems",
            "Sorting property",
            "Greedy property",
            "Randomization"
        ],
        "answer": "Overlapping subproblems"
    }
]

# ==========================================
# FAST + ACCURATE ANSWER FUNCTION
# ==========================================

def answer_question(question):

    prompt = f"""
You are a strict DAA (Design and Analysis of Algorithms) tutor.

Give a correct, exam-ready answer.

Question: {question}

Format:
Definition:
Explanation:
Example:
Time Complexity:
Key Points:
"""

    try:
        result = generator(
            prompt,
            max_new_tokens=180,   # 🔥 faster
            do_sample=False,      # 🔥 more accurate (no randomness)
            temperature=0.2       # 🔥 stable output
        )

        text = result[0]["generated_text"]

        # remove prompt safely
        answer = text.replace(prompt, "").strip()

        return answer

    except Exception as e:
        return f"Error: {e}"

# ==========================================
# QUIZ FUNCTION
# ==========================================

def generate_quiz():
    return random.choice(quiz_bank)

# ==========================================
# UI
# ==========================================

output = widgets.Output()

question_box = widgets.Text(
    placeholder="Ask DAA question...",
    description="Question:",
    layout=widgets.Layout(width='85%')
)

ask_btn = widgets.Button(description="Ask AI", button_style="success")
quiz_btn = widgets.Button(description="Quiz", button_style="info")
clear_btn = widgets.Button(description="Clear", button_style="warning")

# ==========================================
# ASK FUNCTION
# ==========================================

def on_ask(b):
    with output:
        clear_output()

        q = question_box.value.strip()
        if not q:
            print("Enter a question.")
            return

        print("Generating answer...\n")
        print(answer_question(q))

ask_btn.on_click(on_ask)

# ==========================================
# QUIZ FUNCTION
# ==========================================

def on_quiz(b):
    with output:
        clear_output()

        quiz = generate_quiz()

        print("DAA MCQ QUIZ\n")
        print(quiz["question"])

        options = widgets.RadioButtons(options=quiz["options"])

        submit = widgets.Button(description="Submit", button_style="primary")
        result = widgets.Output()

        def check(_):
            with result:
                clear_output()
                if options.value == quiz["answer"]:
                    print("Correct ✅")
                else:
                    print("Wrong ❌")
                    print("Answer:", quiz["answer"])

        submit.on_click(check)

        display(widgets.VBox([options, submit, result]))

quiz_btn.on_click(on_quiz)

# ==========================================
# CLEAR
# ==========================================

def on_clear(b):
    with output:
        clear_output()
    question_box.value = ""

clear_btn.on_click(on_clear)

# ==========================================
# UI LAYOUT
# ==========================================

title = widgets.HTML("<h2>🎓 Fast AI DAA Tutor</h2>")

display(widgets.VBox([
    title,
    question_box,
    widgets.HBox([ask_btn, quiz_btn, clear_btn]),
    output
]))
