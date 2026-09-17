from app.agents.registry import AgentRegistry
from app.memory.manager import MemoryManager
from app.models.state import AIState


class Orchestrator:

    def __init__(
        self,
        registry: AgentRegistry,
        memory: MemoryManager,
    ):
        self.registry = registry
        self.memory = memory

    def route(self, state: AIState) -> str:
        """
        Determine which agent should handle the task.

        V1 uses a deterministic planner route.
        Future versions can use an AI-powered router.
        """
        return "planner"

    def run(self, state: AIState) -> AIState:
        agent_name = self.route(state)
        agent = self.registry.get(agent_name)

        state["current_agent"] = agent_name
        state["memory"] = self.memory

        return agent.run(state)
