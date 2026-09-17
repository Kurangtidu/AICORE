from app.models.state import AIState


def test_ai_state():
    state: AIState = {
        "task": "Test AI Core",
        "response": "",
        "current_agent": "base",
        "messages": [],
        "metadata": {},
    }

    assert state["task"] == "Test AI Core"
    assert state["current_agent"] == "base"
    assert isinstance(state["messages"], list)
    assert isinstance(state["metadata"], dict)
