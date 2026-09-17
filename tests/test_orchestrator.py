from app.agents.planner import PlannerAgent
from app.agents.registry import AgentRegistry
from app.core.orchestrator import Orchestrator
from app.memory.local import LocalMemory
from app.memory.manager import MemoryManager


def fake_ai(prompt: str) -> str:
    return "1. Pelajari Python\n2. Latihan coding\n3. Buat proyek"


def create_orchestrator():
    registry = AgentRegistry()
    registry.register(PlannerAgent(ai_func=fake_ai))

    memory = MemoryManager(LocalMemory())

    return Orchestrator(
        registry=registry,
        memory=memory,
    )


def test_orchestrator_route():
    orchestrator = create_orchestrator()

    state = {
        "task": "Test AI Core",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    assert orchestrator.route(state) == "planner"


def test_orchestrator_run():
    orchestrator = create_orchestrator()

    state = {
        "task": "Buat rencana belajar Python",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = orchestrator.run(state)

    assert result["current_agent"] == "planner"
    assert result["response"]
    assert result["memory"] is not None

def test_orchestrator_routes_to_researcher():
    from app.agents.researcher import ResearchAgent
    from app.core.router import Router
    from app.memory.local import LocalMemory
    from app.memory.manager import MemoryManager

    def fake_ai(prompt: str) -> str:
        return "Hasil riset tentang LangGraph."

    registry = AgentRegistry()
    registry.register(ResearchAgent(ai_func=fake_ai))

    memory = MemoryManager(LocalMemory())

    orchestrator = Orchestrator(
        registry=registry,
        memory=memory,
        router=Router(),
    )

    state = {
        "task": "Riset tentang LangGraph",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = orchestrator.run(state)

    assert result["current_agent"] == "researcher"
    assert result["response"] == "Hasil riset tentang LangGraph."
    assert result["memory"].get("research:last_result") == (
        "Hasil riset tentang LangGraph."
    )
