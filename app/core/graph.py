from langgraph.graph import StateGraph, START, END

from app.agents.registry import AgentRegistry, create_default_registry
from app.core.router import Router
from app.memory.supabase import SupabaseMemory
from app.memory.manager import MemoryManager
from app.models.state import AIState
from app.tools.registry import (
    ToolRegistry,
    create_default_tool_registry,
)


def build_graph(
    registry: AgentRegistry | None = None,
    memory: MemoryManager | None = None,
    tool_registry: ToolRegistry | None = None,
):
    if registry is None:
        registry = create_default_registry()

    if memory is None:
        memory_store = SupabaseMemory()
        memory = MemoryManager(memory_store)

    if tool_registry is None:
        tool_registry = create_default_tool_registry()

    router = Router()

    def orchestrator_node(state: AIState) -> AIState:
        task = state.get("task", "")
        state["current_agent"] = router.route(state)

        research_keywords = [
            "riset",
            "research",
            "cari tahu",
            "penelitian",
            "sumber",
            "referensi",
        ]

        coding_keywords = [
            "kode",
            "coding",
            "program",
            "programming",
            "buatkan code",
            "buat kode",
            "debug",
            "perbaiki code",
        ]

        task_lower = task.lower()

        wants_research = any(
            keyword in task_lower
            for keyword in research_keywords
        )

        wants_coding = any(
            keyword in task_lower
            for keyword in coding_keywords
        )

        if wants_research and wants_coding:
            state["current_agent"] = "researcher"

        return state

    def research_node(state: AIState) -> AIState:
        state["memory"] = memory
        agent = registry.get("researcher")
        return agent.run(state)

    def coder_node(state: AIState) -> AIState:
        state["memory"] = memory
        agent = registry.get("coder")
        agent.tool_registry = tool_registry
        return agent.run(state)

    def planner_node(state: AIState) -> AIState:
        state["memory"] = memory
        agent = registry.get("planner")
        return agent.run(state)

    def route_after_orchestrator(state: AIState) -> str:
        agent = state.get("current_agent", "planner")

        if agent == "researcher":
            return "researcher"

        if agent == "coder":
            return "coder"

        return "planner"

    def route_after_research(state: AIState) -> str:
        task = state.get("task", "").lower()

        coding_keywords = [
            "kode",
            "coding",
            "program",
            "programming",
            "buatkan code",
            "buat kode",
            "debug",
            "perbaiki code",
        ]

        if any(
            keyword in task
            for keyword in coding_keywords
        ):
            return "coder"

        return "end"

    graph = StateGraph(AIState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("researcher", research_node)
    graph.add_node("coder", coder_node)
    graph.add_node("planner", planner_node)

    graph.add_edge(START, "orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {
            "researcher": "researcher",
            "coder": "coder",
            "planner": "planner",
        },
    )

    graph.add_conditional_edges(
        "researcher",
        route_after_research,
        {
            "coder": "coder",
            "end": END,
        },
    )

    graph.add_edge("coder", END)
    graph.add_edge("planner", END)

    return graph.compile()


graph = build_graph()
