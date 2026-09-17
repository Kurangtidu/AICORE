from collections.abc import Callable

from app.agents.base import BaseAgent
from app.core.execution import (
    fail_agent,
    finish_agent,
    start_agent,
)
from app.core.llm import ask_ai
from app.models.state import AIState


class PlannerAgent(BaseAgent):
    name = "planner"

    def __init__(self, ai_func: Callable[[str], str] = ask_ai):
        self.ai_func = ai_func

    def run(self, state: AIState) -> AIState:
        start_agent(state, self.name)

        try:
            task = state["task"]
            memory = state.get("memory")

            previous_plan = None

            if memory is not None:
                previous_plan = memory.get("planner:last_plan")

            context = ""

            if previous_plan:
                context = f"""
A previous plan exists in memory:

{previous_plan}

Improve or adapt it when useful.
"""

            prompt = f"""
You are the Planner Agent of an AI orchestration system.
Create a clear, concise step-by-step plan for this task:

{task}

{context}

Return only the plan.
"""

            plan = self.ai_func(prompt)

            state["current_agent"] = self.name
            state["response"] = plan

            state["messages"].append({
                "agent": self.name,
                "content": plan,
            })

            if memory is not None:
                memory.save("planner:last_plan", plan)

            finish_agent(state, self.name)

            return state

        except Exception as exc:
            fail_agent(
                state,
                self.name,
                str(exc),
            )
            raise
