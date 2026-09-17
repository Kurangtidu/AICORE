import os
from typing import Any

from dotenv import load_dotenv
from supabase import create_client

from app.memory.base import MemoryStore


load_dotenv()


class SupabaseMemory(MemoryStore):

    def __init__(self):
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_KEY"]

        self.client = create_client(url, key)

    def save(self, key: str, value: Any) -> None:
        self.client.table("ai_memory").upsert(
            {
                "memory_key": key,
                "memory_value": value,
            },
            on_conflict="memory_key",
        ).execute()

    def get(self, key: str) -> Any:
        result = (
            self.client
            .table("ai_memory")
            .select("memory_value")
            .eq("memory_key", key)
            .limit(1)
            .execute()
        )

        if not result.data:
            return None

        return result.data[0]["memory_value"]

    def delete(self, key: str) -> None:
        (
            self.client
            .table("ai_memory")
            .delete()
            .eq("memory_key", key)
            .execute()
        )
