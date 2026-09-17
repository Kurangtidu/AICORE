from app.agents.coder import CoderAgent
from app.models.state import AIState


def fake_ai(prompt: str) -> str:
    return "def hello():\n    return 'Hello World'"


def test_coder_agent():
    agent = CoderAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Buat fungsi Python sederhana",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "coder"
    assert result["response"] == (
        "def hello():\n"
        "    return 'Hello World'"
    )
    assert len(result["messages"]) == 1
    assert result["messages"][0]["agent"] == "coder"
