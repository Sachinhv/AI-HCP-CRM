from app.tools.search_history import search_history

history = [
    {
        "date": "2026-07-01",
        "topic": "Product X",
        "sentiment": "Positive"
    },
    {
        "date": "2026-07-08",
        "topic": "Product Y",
        "sentiment": "Neutral"
    }
]

print(search_history("Dr. John", history))