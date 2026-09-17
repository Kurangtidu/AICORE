from app.core.execution import (
    fail_agent,
    finish_agent,
    start_agent,
)
from app.models.state import AIState


def test_start_agent():
    state: AIState = {}

    result = start_agent(state, "researcher")

    assert result["current_agent"] == "researcher"
    assert result["status"] == "running"
    assert result["agent_history"] == ["researcher"]


def test_multiple_agents():
    state: AIState = {}

    start_agent(state, "researcher")
    start_agent(state, "coder")

    assert state["agent_history"] == [
        "researcher",
        "coder",
    ]


def test_finish_agent():
    state: AIState = {}

    start_agent(state, "coder")
    result = finish_agent(state, "coder")

    assert result["current_agent"] == "coder"
    assert result["status"] == "completed"


def test_fail_agent():
    state: AIState = {}

    start_agent(state, "coder")
    result = fail_agent(
        state,
        "coder",
        "Compilation failed",
    )

    assert result["current_agent"] == "coder"
    assert result["status"] == "failed"
    assert result["error"] == "Compilation failed"
