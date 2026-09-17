from app.models.state import AIState


class Router:

    def route(self, state: AIState) -> str:
        """
        Determine which registered agent should handle the task.

        V1 uses deterministic routing.
        Planner is the default fallback until more agents are added.
        """
        task = state.get("task", "").lower()

        planning_keywords = [
            "rencana",
            "planning",
            "plan",
            "langkah",
            "strategi",
            "belajar",
        ]

        if any(keyword in task for keyword in planning_keywords):
            return "planner"

        return "planner"
