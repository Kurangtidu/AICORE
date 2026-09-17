from typing import Any, TypedDict


class AIState(TypedDict, total=False):
    task: str
    plan: str
    research: str
    response: str
    current_agent: str
    memory: Any
    messages: list[dict[str, Any]]
    metadata: dict[str, Any]
