
from app.agents.base import BaseAgent
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise KeyError(f"Agent not registered: {name}")

        return self._agents[name]

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())


def create_default_registry() -> AgentRegistry:
    registry = AgentRegistry()

    registry.register(PlannerAgent())
    registry.register(ResearchAgent())

    return registry
