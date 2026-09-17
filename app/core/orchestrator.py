from app.agents.registry import AgentRegistry
from app.core.router import Router
from app.memory.manager import MemoryManager
from app.models.state import AIState


class Orchestrator:

    def __init__(
        self,
        registry: AgentRegistry,
        memory: MemoryManager,
        router: Router | None = None,
    ):
        self.registry = registry
        self.memory = memory
        self.router = router or Router()

    def route(self, state: AIState) -> str:
        """
        Determine which agent should handle the task.
        """
        return self.router.route(state)

    def run(self, state: AIState) -> AIState:
        agent_name = self.route(state)
        agent = self.registry.get(agent_name)

        state["current_agent"] = agent_name
        state["memory"] = self.memory

        return agent.run(state)
