from app.langgraph.graph import crm_graph


def run_agent(user_input: str):

    result = crm_graph.invoke(
        {
            "user_input": user_input,
            "tool": "",
            "result": {}
        }
    )

    return result