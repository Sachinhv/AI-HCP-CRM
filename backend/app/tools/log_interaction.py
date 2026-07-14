import json
from app.services.groq_service import ask_llm


def log_interaction(user_input: str):
    prompt = f"""
You are an AI CRM assistant.

Extract the following information.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT explain anything.

Fields:
- hcp_name
- interaction_type
- date
- time
- attendees
- topics_discussed
- materials_shared
- samples_distributed
- sentiment
- outcomes
- follow_up

Conversation:
{user_input}
"""

    response = ask_llm(prompt)

    # Remove markdown code fences if present
    response = response.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(response)
    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response
        }