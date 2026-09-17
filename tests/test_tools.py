from app.tools.base import BaseTool
from app.tools.registry import ToolRegistry


class EchoTool(BaseTool):
    name = "echo"
    description = "Returns the provided text."

    def run(self, **kwargs):
        return kwargs.get("text", "")


def test_tool_registry():
    registry = ToolRegistry()
    tool = EchoTool()

    registry.register(tool)

    assert registry.list_tools() == ["echo"]
    assert registry.get("echo") is tool
    assert tool.run(text="hello") == "hello"


def test_tool_registry_missing_tool():
    registry = ToolRegistry()

    try:
        registry.get("missing")
        assert False, "Seharusnya ToolRegistry gagal"
    except KeyError as exc:
        assert "Tool not registered" in str(exc)
