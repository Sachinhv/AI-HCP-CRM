from app.tools.summarize import summarize_interaction

interaction = {
    "hcp_name": "Dr. John",
    "interaction_type": "Meeting",
    "topics_discussed": ["Product X"],
    "sentiment": "Positive",
    "materials_shared": ["Brochure"],
    "follow_up": "Meet again next week"
}

summary = summarize_interaction(interaction)

print(summary)