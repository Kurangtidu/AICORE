from app.memory.local import LocalMemory


def test_local_memory():
    memory = LocalMemory()

    memory.save("task", "Test AI Core")

    assert memory.get("task") == "Test AI Core"


def test_local_memory_delete():
    memory = LocalMemory()

    memory.save("task", "Test AI Core")
    memory.delete("task")

    assert memory.get("task") is None
