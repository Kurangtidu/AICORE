from app.agents.planner import PlannerAgent
from app.agents.registry import AgentRegistry, create_default_registry


def test_register_and_get_agent():
    registry = AgentRegistry()
    planner = PlannerAgent()

    registry.register(planner)

    assert registry.get("planner") is planner


def test_default_registry():
    registry = create_default_registry()

    assert "planner" in registry.list_agents()
    assert isinstance(registry.get("planner"), PlannerAgent)
