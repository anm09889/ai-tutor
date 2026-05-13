import streamlit as st
import random

st.set_page_config(page_title="AI Quiz Tutor", layout="wide")

# =========================
# QUIZ DATABASE (10+ QUESTIONS EACH)
# =========================
quiz_data = {
    "sorting": [
        {"question": "Time complexity of Merge Sort?", "options": ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], "answer": "O(n log n)"},
        {"question": "Quick Sort worst case?", "options": ["O(n²)", "O(n)", "O(log n)", "O(n log n)"], "answer": "O(n²)"},
        {"question": "Which is stable?", "options": ["Quick Sort", "Merge Sort", "Heap Sort", "Selection Sort"], "answer": "Merge Sort"},
        {"question": "Which is divide and conquer?", "options": ["Bubble Sort", "Merge Sort", "Insertion Sort", "Linear Search"], "answer": "Merge Sort"},
        {"question": "Best case Quick Sort?", "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "answer": "O(n log n)"},
        {"question": "Heap Sort complexity?", "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "answer": "O(n log n)"},
        {"question": "Bubble sort best case?", "options": ["O(n)", "O(n²)", "O(log n)", "O(n log n)"], "answer": "O(n)"},
        {"question": "Insertion sort worst case?", "options": ["O(n²)", "O(n)", "O(log n)", "O(n log n)"], "answer": "O(n²)"},
        {"question": "Which is in-place?", "options": ["Merge Sort", "Quick Sort", "Counting Sort", "Radix Sort"], "answer": "Quick Sort"},
        {"question": "Which uses recursion?", "options": ["Merge Sort", "Queue", "Stack", "Array"], "answer": "Merge Sort"},
    ],

    "searching": [
        {"question": "Binary search works on?", "options": ["Unsorted array", "Sorted array", "Graph", "Tree"], "answer": "Sorted array"},
        {"question": "Linear search complexity?", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "answer": "O(n)"},
        {"question": "Binary search complexity?", "options": ["O(log n)", "O(n)", "O(n²)", "O(1)"], "answer": "O(log n)"},
        {"question": "Best case linear search?", "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"], "answer": "O(1)"},
        {"question": "Binary search uses?", "options": ["Divide and conquer", "Greedy", "DP", "Backtracking"], "answer": "Divide and conquer"},
        {"question": "Which is faster?", "options": ["Linear", "Binary", "DFS", "BFS"], "answer": "Binary"},
        {"question": "Binary search needs?", "options": ["Sorted array", "Tree", "Graph", "Stack"], "answer": "Sorted array"},
        {"question": "Worst case binary search?", "options": ["O(log n)", "O(n)", "O(n²)", "O(1)"], "answer": "O(log n)"},
        {"question": "Linear search works on?", "options": ["Any array", "Sorted only", "Graph", "Tree"], "answer": "Any array"},
        {"question": "Binary search compares?", "options": ["Middle element", "First element", "Last element", "Random"], "answer": "Middle element"},
    ]
}

# =========================
# UI
# =========================
st.title("🎓 AI Quiz Tutor (Topic Based)")

topic = st.text_input("Enter Topic (sorting / searching)")

if st.button("Start Quiz"):

    if topic.lower() not in quiz_data:
        st.error("Topic not found!")
    else:
        questions = random.sample(quiz_data[topic.lower()], 10)

        score = 0
        user_answers = []

        for i, q in enumerate(questions):
            st.subheader(f"Q{i+1}: {q['question']}")
            choice = st.radio(f"Select answer {i+1}", q["options"], key=i)

            user_answers.append(choice)

        if st.button("Submit Quiz"):

            for i, q in enumerate(questions):
                if user_answers[i] == q["answer"]:
                    score += 1

            st.success(f"Your Score: {score}/10")

            st.write("### Review")
            for i, q in enumerate(questions):
                st.write(f"Q{i+1}: {q['question']}")
                st.write(f"✔ Correct: {q['answer']}")
                st.write(f"❌ Your Answer: {user_answers[i]}")
                st.write("---")
