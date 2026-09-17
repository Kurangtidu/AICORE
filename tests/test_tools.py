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


def test_calculator_tool():
    from app.tools.calculator import CalculatorTool

    tool = CalculatorTool()

    assert tool.run("2 + 3") == "5"
    assert tool.run("10 * 5") == "50"
    assert tool.run("100 / 4") == "25.0"


def test_calculator_invalid_expression():
    from app.tools.calculator import CalculatorTool

    tool = CalculatorTool()

    result = tool.run("invalid expression")

    assert result.startswith("Calculation error:")


def test_calculator_blocks_unsafe_expression():
    from app.tools.calculator import CalculatorTool

    tool = CalculatorTool()

    result = tool.run("__import__('os').system('echo hacked')")

    assert result.startswith("Calculation error:")


def test_default_tool_registry():
    from app.tools.registry import create_default_tool_registry

    registry = create_default_tool_registry()

    assert registry.list_tools() == ["calculator"]
    assert registry.get("calculator").name == "calculator"
