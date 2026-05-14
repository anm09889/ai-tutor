import random

def ai_engine(query):

    q = query.lower()

    # ---------------------------
    # DBMS / TECH CATEGORY
    # ---------------------------
    if "dbms" in q or "database" in q:

        responses = [
            f"""
DBMS (Database Management System) is basically software that helps store and manage data efficiently.

Think of it like a digital library where data is organized so it can be easily accessed, updated, and managed.
It is used in applications like banking systems, websites, and apps.
""",

            f"""
A DBMS is a system that controls how data is stored and retrieved.

In simple terms, it acts like a smart organizer for large amounts of data.
For example, when you use Instagram or banking apps, DBMS is working behind the scenes.
""",

            f"""
Database Management System (DBMS) is used to handle large collections of data.

It ensures data is stored safely, retrieved quickly, and managed properly.
Without DBMS, handling large systems like social media or e-commerce would be impossible.
"""
        ]

        return random.choice(responses)

    # ---------------------------
    # DSA CATEGORY
    # ---------------------------
    elif any(word in q for word in ["sorting", "array", "tree", "graph", "algorithm"]):

        responses = [
            f"""
This topic relates to data structures and algorithms.

It focuses on organizing data and solving problems efficiently using step-by-step logic.

Example: Sorting arranges data, while trees and graphs represent relationships.
""",

            f"""
In computer science, this concept is used to optimize problem-solving.

It helps reduce time complexity and improve performance of programs.

Real use: search engines, maps, and AI systems.
""",

            f"""
This is a fundamental programming concept.

It teaches how to structure data and apply logic to solve problems efficiently.

It is widely used in software development and system design.
"""
        ]

        return random.choice(responses)

    # ---------------------------
    # SCIENCE CATEGORY
    # ---------------------------
    elif any(word in q for word in ["physics", "force", "energy", "motion"]):

        responses = [
            f"""
This is a physics concept that explains how the natural world behaves.

It describes how objects move, interact, and respond to forces.

Example: motion of a car or falling objects.
""",

            f"""
In physics, this concept helps us understand energy and movement.

It is based on natural laws and mathematical formulas.

It is used in engineering, space science, and machines.
"""
        ]

        return random.choice(responses)

    # ---------------------------
    # GENERAL CASE (SMART FALLBACK)
    # ---------------------------
    else:

        responses = [
            f"""
Let’s understand this step-by-step.

{query} is an important concept that can be learned by breaking it into smaller ideas.

Once you understand the basics, it becomes easy to apply in real situations.
""",

            f"""
Good question.

{query} is something you can understand by focusing on its core idea first, then examples.

Most concepts become clear when you connect them with real-world use cases.
""",

            f"""
This topic can be explained in a simple way.

Start with the definition, then understand how it works, and finally see where it is used.

That approach makes learning much easier.
"""
        ]

        return random.choice(responses)
