import streamlit as st
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Fast AI Tutor",
    page_icon="⚡",
    layout="wide"
)

# =========================
# FAST AI ENGINE (NO API)
# =========================
def fast_tutor(question):

    q = question.lower()

    # --- DSA TOPICS ---
    if "sorting" in q:
        return """
📘 Sorting Algorithms

✔ Definition:
Sorting means arranging data in order (ascending/descending).

✔ Types:
- Bubble Sort
- Merge Sort
- Quick Sort

✔ Working:
Compare elements and rearrange step by step.

✔ Time Complexity:
- Bubble: O(n²)
- Merge: O(n log n)

✔ Example:
Arranging marks in ascending order.
"""

    elif "dynamic programming" in q:
        return """
📘 Dynamic Programming

✔ Definition:
Technique to solve problems by breaking into subproblems.

✔ Idea:
Store results of subproblems to avoid repetition.

✔ Steps:
1. Break problem
2. Store results
3. Reuse results

✔ Example:
Fibonacci sequence optimization

✔ Complexity:
Improves exponential → linear
"""

    elif "array" in q:
        return """
📘 Arrays

✔ Definition:
Collection of similar data types stored in memory.

✔ Example:
int arr[5] = {1,2,3,4,5}

✔ Operations:
- Access: O(1)
- Insert: O(n)
- Delete: O(n)

✔ Use:
Used in almost every program.
"""

    elif "dbms" in q:
        return """
📘 DBMS

✔ Definition:
Database Management System stores and manages data.

✔ Features:
- Data security
- Fast retrieval
- Backup

✔ Types:
- Relational DBMS
- NoSQL

✔ Example:
MySQL, MongoDB
"""

    else:
        return f"""
📘 Explanation of: {question}

✔ Simple Idea:
This topic is important in Computer Science.

✔ How it works:
It follows step-by-step logical processing.

✔ Key Points:
- Understand concept
- Learn examples
- Practice problems

✔ Tip:
Focus on understanding, not memorization.
"""

# =========================
# UI
# =========================
st.title("⚡ Fast AI Tutor (Instant Answers)")

question = st.text_input("Ask your question (DSA / DBMS / AI / OS etc.)")

if st.button("Get Fast Answer"):

    if question:

        with st.spinner("Generating fast explanation..."):
            time.sleep(0.3)  # very small delay for UX
            answer = fast_tutor(question)

        st.success(answer)

    else:
        st.warning("Please enter a question")

# =========================
# QUICK HELP SECTION
# =========================
st.markdown("---")
st.subheader("💡 Supported Topics (Fast Mode)")

st.write("""
✔ Sorting  
✔ Arrays  
✔ Dynamic Programming  
✔ DBMS  
✔ OS  
✔ Any general CS question
""")
