from app.agents.researcher import ResearchAgent
from app.models.state import AIState


def fake_ai(prompt: str) -> str:
    return "LangGraph adalah framework untuk membangun workflow dan agent AI."


def test_researcher_agent():
    agent = ResearchAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Riset tentang LangGraph",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "researcher"
    assert result["response"] == (
        "LangGraph adalah framework untuk membangun workflow dan agent AI."
    )
    assert len(result["messages"]) == 1
    assert result["messages"][0]["agent"] == "researcher"
