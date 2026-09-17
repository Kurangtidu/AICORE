from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    name: str = "base"
    description: str = ""

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError
