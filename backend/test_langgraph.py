from app.langgraph.agent import run_agent

print(run_agent(
    "Today I met Dr. Smith. Discussed Product X."
))

print(run_agent(
    "Give me summary."
))

print(run_agent(
    "Suggest follow up."
))

print(run_agent(
    "Show previous history."
))