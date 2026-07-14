from app.services.groq_service import ask_llm


def suggest_followup(interaction_data: dict):

    prompt = f"""
You are an experienced pharmaceutical CRM assistant.

Based on the interaction below, suggest the next follow-up actions.

Interaction:

{interaction_data}

Return ONLY 3 concise follow-up suggestions.
"""

    return ask_llm(prompt)