from app.tools.edit_interaction import edit_interaction

existing = {
    "hcp_name": "Dr. Smith",
    "interaction_type": "Meeting",
    "date": "Today",
    "sentiment": "Positive",
    "topics_discussed": ["Product X"],
    "materials_shared": ["Brochure"]
}

result = edit_interaction(
    existing,
    "Actually the doctor's name is Dr. John and the sentiment was negative."
)

print(result)