from app.agents.coder import CoderAgent
from app.models.state import AIState


def fake_ai(prompt: str) -> str:
    return "def hello():\n    return 'Hello World'"


def test_coder_agent():
    agent = CoderAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Buat fungsi Python sederhana",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "coder"
    assert result["response"] == (
        "def hello():\n"
        "    return 'Hello World'"
    )
    assert len(result["messages"]) == 1
    assert result["messages"][0]["agent"] == "coder"

def test_coder_uses_research_result():
    captured_prompt = {}

    def fake_ai(prompt: str) -> str:
        captured_prompt["value"] = prompt
        return "Implementasi berdasarkan hasil riset."

    agent = CoderAgent(ai_func=fake_ai)

    state: AIState = {
        "task": "Implementasikan hasil riset",
        "research": "LangGraph menggunakan StateGraph untuk workflow agent.",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    }

    result = agent.run(state)

    assert result["current_agent"] == "coder"
    assert result["response"] == "Implementasi berdasarkan hasil riset."
    assert "LangGraph menggunakan StateGraph untuk workflow agent." in (
        captured_prompt["value"]
    )


def test_coder_receives_tool_registry():
    from app.tools.registry import create_default_tool_registry

    registry = create_default_tool_registry()
    agent = CoderAgent(
        ai_func=fake_ai,
        tool_registry=registry,
    )

    assert agent.tool_registry is registry


def test_coder_can_use_calculator_tool():
    from app.tools.registry import create_default_tool_registry

    registry = create_default_tool_registry()

    agent = CoderAgent(
        ai_func=fake_ai,
        tool_registry=registry,
    )

    result = agent.tool_registry.get("calculator").run(
        expression="10 * 5"
    )

    assert result == "50"


def test_coder_can_invoke_calculator():
    from app.tools.registry import create_default_tool_registry

    registry = create_default_tool_registry()

    agent = CoderAgent(
        ai_func=fake_ai,
        tool_registry=registry,
    )

    result = agent.use_tool(
        "calculator",
        expression="25 * 4",
    )

    assert result == "100"


def test_coder_tool_invocation_returns_result():
    from app.tools.registry import create_default_tool_registry

    registry = create_default_tool_registry()

    agent = CoderAgent(
        ai_func=fake_ai,
        tool_registry=registry,
    )

    result = agent.invoke_tool(
        tool_name="calculator",
        arguments={
            "expression": "125 * 8",
        },
    )

    assert result == "1000"
