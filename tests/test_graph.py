from app.agents.planner import PlannerAgent
from app.agents.registry import AgentRegistry
from app.core.graph import build_graph
from app.memory.local import LocalMemory
from app.memory.manager import MemoryManager


def fake_ai(prompt: str) -> str:
    return "1. Pelajari Python\n2. Latihan coding\n3. Buat proyek"


def test_ai_core_graph():
    registry = AgentRegistry()
    registry.register(PlannerAgent(ai_func=fake_ai))

    memory = MemoryManager(LocalMemory())

    graph = build_graph(
        registry=registry,
        memory=memory,
    )

    result = graph.invoke({
        "task": "Buat rencana belajar Python untuk pemula",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    })

    assert result["current_agent"] == "planner"
    assert result["response"]
    assert len(result["messages"]) == 1
    assert result["messages"][0]["agent"] == "planner"
