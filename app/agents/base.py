from abc import ABC, abstractmethod

from app.models.state import AIState


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    def run(self, state: AIState) -> AIState:
        """Execute the agent and return the updated state."""
        raise NotImplementedError
