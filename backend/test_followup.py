from app.tools.followup import suggest_followup

interaction = {
    "hcp_name": "Dr. John",
    "topics_discussed": ["Product X"],
    "sentiment": "Positive"
}

print(suggest_followup(interaction))