import streamlit as st
import time
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Universal AI Tutor",
    page_icon="🧠",
    layout="wide"
)

# =========================
# MODERN UI
# =========================
st.markdown("""
<style>
.main {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #4ade80;
}

.card {
    background: #111827;
    padding: 18px;
    border-radius: 12px;
    margin-top: 10px;
    color: white;
}

.small {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# =========================
# UNIVERSAL AI ENGINE (SMART FALLBACK)
# =========================
def ai_engine(query):

    q = query.lower()

    # --- MATH / TECH ---
    if any(word in q for word in ["algorithm", "sorting", "dp", "array", "tree", "graph"]):
        return f"""
📘 TECH EXPLANATION

✔ Topic: {query}

✔ Definition:
This is a computer science concept used to solve structured problems.

✔ Key Idea:
Break problems → process step-by-step → optimize solution.

✔ Real Use:
- Software development
- AI systems
- Search engines

✔ Complexity Insight:
Depends on algorithm design (often O(n), O(log n), O(n²))
"""

    # --- SCIENCE ---
    elif any(word in q for word in ["physics", "force", "energy", "motion", "gravity"]):
        return f"""
🔬 SCIENCE EXPLANATION

✔ Topic: {query}

✔ Concept:
This is a physics-related concept describing natural behavior.

✔ Explanation:
It explains how objects interact in the real world.

✔ Example:
Used in motion, machines, and space systems.

✔ Key Insight:
Based on laws of nature and mathematical models.
"""

    # --- GENERAL KNOWLEDGE ---
    elif any(word in q for word in ["india", "history", "who", "capital", "president"]):
        return f"""
🌍 GENERAL KNOWLEDGE

✔ Topic: {query}

✔ Answer:
This is a factual real-world concept.

✔ Explanation:
It belongs to general knowledge and factual learning.

✔ Tip:
Always verify facts from trusted sources.
"""

    # --- DEFAULT SMART AI RESPONSE ---
    else:
        return f"""
🧠 SMART EXPLANATION

✔ Question:
{query}

✔ Simple Answer:
This concept is part of general learning and can be understood step-by-step.

✔ Breakdown:
1. Understand the topic
2. Break into smaller parts
3. Learn with examples
4. Apply in real life

✔ Insight:
Most concepts become easy when connected with real-world examples.

✔ Tip:
Focus on logic, not memorization.
"""

# =========================
# HEADER
# =========================
st.markdown('<div class="main">🧠 Universal AI Tutor</div>', unsafe_allow_html=True)
st.write("Ask anything — AI will explain in simple + structured way")

# =========================
# INPUT
# =========================
question = st.text_input("Enter your question (any subject)")

# =========================
# ANSWER BUTTON
# =========================
if st.button("Get Answer"):

    if question:

        with st.spinner("Thinking deeply..."):
            time.sleep(0.6)

            answer = ai_engine(question)

        st.markdown(f"""
        <div class="card">
        {answer}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Please enter a question")

# =========================
# FOOTER HELP
# =========================
st.markdown("---")
st.markdown("<p class='small'>Supports: DSA, Science, GK, Math, Technology, and general questions</p>", unsafe_allow_html=True)
