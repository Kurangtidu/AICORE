from collections.abc import Callable

from app.agents.base import BaseAgent
from app.core.execution import (
    fail_agent,
    finish_agent,
    start_agent,
)
from app.core.llm import ask_ai
from app.models.state import AIState
from app.tools.registry import ToolRegistry


class CoderAgent(BaseAgent):
    name = "coder"

    def __init__(
        self,
        ai_func: Callable[[str], str] = ask_ai,
        tool_registry: ToolRegistry | None = None,
    ):
        self.ai_func = ai_func
        self.tool_registry = tool_registry

    def should_use_tool(self, task: str) -> bool:
        if self.tool_registry is None:
            return False

        calculator_keywords = [
            "hitung",
            "calculate",
            "calculator",
            "perhitungan",
            "berapa hasil",
        ]

        task_lower = task.lower()

        return any(
            keyword in task_lower
            for keyword in calculator_keywords
        )

    def invoke_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):
        return self.use_tool(
            tool_name,
            **arguments,
        )

    def use_tool(self, tool_name: str, **kwargs):
        if self.tool_registry is None:
            raise RuntimeError("Tool registry is not configured")

        tool = self.tool_registry.get(tool_name)
        return tool.run(**kwargs)

    def run(self, state: AIState) -> AIState:
        start_agent(state, self.name)

        try:
            task = state["task"]
            memory = state.get("memory")
            research = state.get("research")

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

            if research:
                context += f"""
Research result from the Researcher Agent:

{research}

Use this research as context when implementing the solution.
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

            finish_agent(state, self.name)

            return state

        except Exception as exc:
            fail_agent(
                state,
                self.name,
                str(exc),
            )
            raise
