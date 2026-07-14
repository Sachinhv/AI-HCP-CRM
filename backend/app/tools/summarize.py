from app.services.groq_service import ask_llm


def summarize_interaction(interaction_data: dict):

    prompt = f"""
You are an AI CRM assistant.

Generate a professional meeting summary using the following interaction.

Interaction:

{interaction_data}

Return ONLY the summary.
"""

    return ask_llm(prompt)