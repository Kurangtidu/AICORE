from app.tools.base import BaseTool
from app.tools.calculator import CalculatorTool


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool not registered: {name}")

        return self._tools[name]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())


def create_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(CalculatorTool())

    return registry
