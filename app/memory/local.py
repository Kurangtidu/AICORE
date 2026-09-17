from typing import Any

from app.memory.base import MemoryStore


class LocalMemory(MemoryStore):

    def __init__(self):
        self._data: dict[str, Any] = {}

    def save(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)
