from app.agents.coder import CoderAgent
from app.agents.registry import AgentRegistry
from app.agents.researcher import ResearchAgent
from app.core.graph import build_graph
from app.memory.local import LocalMemory
from app.memory.manager import MemoryManager
from app.models.state import AIState


def test_research_to_coder_workflow():
    def fake_research(prompt: str) -> str:
        return "Hasil riset: gunakan StateGraph untuk workflow."

    def fake_coder(prompt: str) -> str:
        assert "Hasil riset: gunakan StateGraph untuk workflow." in prompt
        return "Kode dibuat berdasarkan hasil riset."

    registry = AgentRegistry()
    registry.register(ResearchAgent(ai_func=fake_research))
    registry.register(CoderAgent(ai_func=fake_coder))

    memory = MemoryManager(LocalMemory())

    graph = build_graph(
        registry=registry,
        memory=memory,
    )

    state: AIState = {
        "task": "Riset lalu buat kode tentang LangGraph",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = graph.invoke(state)

    assert result["research"] == (
        "Hasil riset: gunakan StateGraph untuk workflow."
    )
    assert result["response"] == (
        "Kode dibuat berdasarkan hasil riset."
    )


def test_execution_history():
    def fake_research(prompt: str) -> str:
        return "Hasil riset."

    def fake_coder(prompt: str) -> str:
        return "Kode selesai."

    registry = AgentRegistry()
    registry.register(ResearchAgent(ai_func=fake_research))
    registry.register(CoderAgent(ai_func=fake_coder))

    memory = MemoryManager(LocalMemory())

    graph = build_graph(
        registry=registry,
        memory=memory,
    )

    state: AIState = {
        "task": "Riset lalu buat kode tentang LangGraph",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = graph.invoke(state)

    assert result["agent_history"] == [
        "researcher",
        "coder",
    ]

    assert result["status"] == "completed"
    assert result["current_agent"] == "coder"
