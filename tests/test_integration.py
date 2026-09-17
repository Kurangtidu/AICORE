import pytest
from app.core.graph import graph
from app.memory.supabase import SupabaseMemory

@pytest.mark.integration
def test_ai_core_end_to_end():
    task = "Buat rencana belajar Python untuk pemula"

    result = graph.invoke({
        "task": task,
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
    })

    assert result["current_agent"] == "planner"
    assert result["response"]
    assert result["messages"]

    memory = SupabaseMemory()
    saved_plan = memory.get("planner:last_plan")

    assert saved_plan == result["response"]

    memory.delete("planner:last_plan")
