from app.agents.base import BaseAgent
from app.models.state import AIState


class TestAgent(BaseAgent):
    name = "test"

    def run(self, state: AIState) -> AIState:
        state["current_agent"] = self.name
        return state


def test_base_agent():
    agent = TestAgent()

    state: AIState = {
        "task": "Test",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "test"
