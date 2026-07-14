from app.services.groq_service import ask_llm

response = ask_llm(
    "Today I met Dr. Smith. We discussed Product X. The sentiment was positive. I shared brochures."
)

print(response)