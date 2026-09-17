from collections.abc import Callable

from app.agents.base import BaseAgent
from app.core.llm import ask_ai
from app.models.state import AIState


class CoderAgent(BaseAgent):
    name = "coder"

    def __init__(self, ai_func: Callable[[str], str] = ask_ai):
        self.ai_func = ai_func

    def run(self, state: AIState) -> AIState:
        task = state["task"]
        memory = state.get("memory")

        previous_code = None

        if memory is not None:
            previous_code = memory.get("coder:last_result")

        context = ""

        if previous_code:
            context = f"""
Previous coding result exists in memory:

{previous_code}

Improve or adapt it when useful.
"""

        prompt = f"""
You are the Coding Agent of an AI orchestration system.

Help solve the following coding task:

{task}

{context}

Provide a clear and practical solution.
Include code when appropriate.
"""

        result = self.ai_func(prompt)

        state["current_agent"] = self.name
        state["response"] = result

        state["messages"].append({
            "agent": self.name,
            "content": result,
        })

        if memory is not None:
            memory.save("coder:last_result", result)

        return state
