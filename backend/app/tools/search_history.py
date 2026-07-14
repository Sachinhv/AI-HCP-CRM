from app.services.groq_service import ask_llm


def search_history(hcp_name: str, history: list):

    prompt = f"""
You are an AI CRM assistant.

Doctor Name:
{hcp_name}

Previous Interactions:
{history}

Summarize the doctor's history in 4-5 lines.
"""

    return ask_llm(prompt)