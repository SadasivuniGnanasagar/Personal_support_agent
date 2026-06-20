import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(query, persona, retrieved_docs):

    context = "\n\n".join(retrieved_docs)

    if persona == "Technical Expert":
        style = """
        Respond as a Senior Support Engineer.
        Give:
        - Root Cause
        - Technical Explanation
        - Troubleshooting Steps
        """

    elif persona == "Frustrated User":
        style = """
        Respond empathetically.
        Use simple language.
        Give clear action steps.
        """

    else:
        style = """
        Respond as a Business Executive Advisor.
        Focus on:
        - Business impact
        - Resolution timeline
        - Concise explanation
        """

    prompt = f"""
    {style}

    Use ONLY the information below:

    Context:
    {context}

    User Question:
    {query}
    """

    response = model.generate_content(prompt)

    return response.text