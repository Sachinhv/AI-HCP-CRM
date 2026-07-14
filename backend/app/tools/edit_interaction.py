import json
from app.services.groq_service import ask_llm


def edit_interaction(existing_data: dict, user_update: str):
    prompt = f"""
You are an AI CRM assistant.

Below is an existing interaction record:

{json.dumps(existing_data, indent=2)}

The user wants to update some fields.

User instruction:
{user_update}

Update ONLY the fields mentioned by the user.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT explain anything.
"""

    response = ask_llm(prompt)

    response = response.replace("```json", "").replace("```", "").strip()

    return json.loads(response)