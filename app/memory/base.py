from abc import ABC, abstractmethod
from typing import Any


class MemoryStore(ABC):

    @abstractmethod
    def save(self, key: str, value: Any) -> None:
        """Save a value to memory."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieve a value from memory."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from memory."""
        raise NotImplementedError
