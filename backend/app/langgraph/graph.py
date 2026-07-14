from langgraph.graph import StateGraph, END

from app.langgraph.state import CRMState

from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.summarize import summarize_interaction
from app.tools.followup import suggest_followup
from app.tools.search_history import search_history


def router(state):

    message = state["user_input"].lower()

    if "edit" in message or "actually" in message:
        tool = "edit"

    elif "summary" in message:
        tool = "summary"

    elif "follow" in message:
        tool = "followup"

    elif "history" in message:
        tool = "history"

    else:
        tool = "log"

    return {
        **state,
        "tool": tool
    }

def tool_node(state: CRMState):

    tool = state["tool"]

    message = state["user_input"]

    if tool == "log":

        result = log_interaction(message)

    elif tool == "summary":

        result = summarize_interaction(
            {"text": message}
        )

    elif tool == "followup":

        result = suggest_followup(
            {"text": message}
        )

    elif tool == "history":

        result = search_history(
            "Dr. John",
            []
        )

    else:

        result = {
            "message": "Edit tool will be connected later."
        }

    return {
        **state,
        "result": result
    }

workflow = StateGraph(CRMState)

workflow.add_node("router", router)
workflow.add_node("tool", tool_node)

workflow.set_entry_point("router")

workflow.add_edge("router", "tool")
workflow.add_edge("tool", END)

crm_graph = workflow.compile()