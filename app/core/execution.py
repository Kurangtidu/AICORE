from app.models.state import AIState


def start_agent(state: AIState, agent_name: str) -> AIState:
    history = state.get("agent_history", [])

    state["current_agent"] = agent_name
    state["status"] = "running"

    state["agent_history"] = [
        *history,
        agent_name,
    ]

    return state


def finish_agent(state: AIState, agent_name: str) -> AIState:
    state["current_agent"] = agent_name
    state["status"] = "completed"

    return state


def fail_agent(
    state: AIState,
    agent_name: str,
    error: str,
) -> AIState:
    state["current_agent"] = agent_name
    state["status"] = "failed"
    state["error"] = error

    return state
