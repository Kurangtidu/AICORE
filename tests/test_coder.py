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

def test_coder_uses_research_result():
    captured_prompt = {}

    def fake_ai(prompt: str) -> str:
        captured_prompt["value"] = prompt
        return "Implementasi berdasarkan hasil riset."

    agent = CoderAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Implementasikan hasil riset",
        "research": "LangGraph menggunakan StateGraph untuk workflow agent.",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "coder"
    assert result["response"] == "Implementasi berdasarkan hasil riset."
    assert "LangGraph menggunakan StateGraph untuk workflow agent." in (
        captured_prompt["value"]
    )
