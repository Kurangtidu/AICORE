from typing import Any

from app.memory.base import MemoryStore


class MemoryManager:

    def __init__(self, store: MemoryStore):
        self.store = store

    def save(self, key: str, value: Any) -> None:
        self.store.save(key, value)

    def get(self, key: str) -> Any:
        return self.store.get(key)

    def delete(self, key: str) -> None:
        self.store.delete(key)
