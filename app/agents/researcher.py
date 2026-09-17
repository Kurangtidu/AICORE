from collections.abc import Callable

from app.agents.base import BaseAgent
from app.core.execution import (
    fail_agent,
    finish_agent,
    start_agent,
)
from app.core.llm import ask_ai
from app.models.state import AIState


class ResearchAgent(BaseAgent):
    name = "researcher"

    def __init__(self, ai_func: Callable[[str], str] = ask_ai):
        self.ai_func = ai_func

    def run(self, state: AIState) -> AIState:
        start_agent(state, self.name)

        try:
            task = state["task"]
            memory = state.get("memory")

            previous_research = None

            if memory is not None:
                previous_research = memory.get("research:last_result")

            context = ""

            if previous_research:
                context = f"""
Previous research exists in memory:

{previous_research}

Use it as context and improve or update it when useful.
"""

            prompt = f"""
You are the Research Agent of an AI orchestration system.

Research and explain the following topic clearly and accurately:

{task}

{context}

Return a concise, structured research result.
"""

            result = self.ai_func(prompt)

            state["current_agent"] = self.name
            state["response"] = result
            state["research"] = result

            state["messages"].append({
                "agent": self.name,
                "content": result,
            })

            if memory is not None:
                memory.save("research:last_result", result)

            finish_agent(state, self.name)

            return state

        except Exception as exc:
            fail_agent(
                state,
                self.name,
                str(exc),
            )
            raise
