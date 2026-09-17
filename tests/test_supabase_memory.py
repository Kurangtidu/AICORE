from app.memory.supabase import SupabaseMemory


def test_supabase_memory_crud():
    memory = SupabaseMemory()

    key = "test:ai-core"
    value = {
        "message": "AI Core Supabase test",
        "status": "ok",
    }

    memory.save(key, value)

    assert memory.get(key) == value

    memory.delete(key)

    assert memory.get(key) is None
