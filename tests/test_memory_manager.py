from app.memory.local import LocalMemory
from app.memory.manager import MemoryManager


def test_memory_manager():
    store = LocalMemory()
    memory = MemoryManager(store)

    memory.save("task", "Test AI Core")

    assert memory.get("task") == "Test AI Core"


def test_memory_manager_delete():
    store = LocalMemory()
    memory = MemoryManager(store)

    memory.save("task", "Test AI Core")
    memory.delete("task")

    assert memory.get("task") is None
