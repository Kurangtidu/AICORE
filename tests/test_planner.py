from app.agents.planner import PlannerAgent
from app.models.state import AIState


def fake_ai(prompt: str) -> str:
    return "1. Pelajari dasar Python\n2. Latihan coding\n3. Buat proyek sederhana"


def test_planner_agent():
    agent = PlannerAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Buat rencana belajar Python untuk pemula",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "planner"
    assert result["response"] == (
        "1. Pelajari dasar Python\n"
        "2. Latihan coding\n"
        "3. Buat proyek sederhana"
    )
    assert len(result["messages"]) == 1
    assert result["messages"][0]["agent"] == "planner"
