from langgraph.graph import StateGraph, START, END

from app.agents.registry import AgentRegistry, create_default_registry
from app.core.orchestrator import Orchestrator
from app.memory.supabase import SupabaseMemory
from app.memory.manager import MemoryManager
from app.models.state import AIState


def build_graph(
    registry: AgentRegistry | None = None,
    memory: MemoryManager | None = None,
):
    if registry is None:
        registry = create_default_registry()

    if memory is None:
        memory_store = SupabaseMemory()
        memory = MemoryManager(memory_store)

    orchestrator = Orchestrator(
        registry=registry,
        memory=memory,
    )

    def orchestrator_node(state: AIState) -> AIState:
        return orchestrator.run(state)

    graph = StateGraph(AIState)

    graph.add_node("orchestrator", orchestrator_node)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", END)

    return graph.compile()


graph = build_graph()
