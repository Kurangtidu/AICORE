from app.agents.planner import PlannerAgent
from app.memory.local import LocalMemory
from app.memory.manager import MemoryManager


def fake_ai(prompt: str) -> str:
    if "previous plan exists in memory" in prompt:
        return "1. Review rencana sebelumnya\n2. Latihan Python\n3. Buat proyek sederhana"

    return "1. Pelajari syntax Python\n2. Latihan membuat program\n3. Buat proyek sederhana"


def test_planner_saves_plan_to_memory():
    planner = PlannerAgent(ai_func=fake_ai)

    memory = MemoryManager(LocalMemory())

    state = {
        "task": "Buat rencana belajar Python",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
        "memory": memory,
    }

    result = planner.run(state)

    saved_plan = memory.get("planner:last_plan")

    assert result["response"]
    assert saved_plan == result["response"]


def test_planner_reads_previous_memory():
    planner = PlannerAgent(ai_func=fake_ai)

    memory = MemoryManager(LocalMemory())

    previous_plan = "1. Pelajari syntax Python\n2. Latihan membuat program"

    memory.save("planner:last_plan", previous_plan)

    state = {
        "task": "Lanjutkan belajar Python",
        "response": "",
        "current_agent": "",
        "messages": [],
        "metadata": {},
        "memory": memory,
    }

    result = planner.run(state)

    assert result["response"]
    assert result["response"] != previous_plan
    assert memory.get("planner:last_plan") == result["response"]
