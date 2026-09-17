from app.models.state import AIState


class Router:

    def route(self, state: AIState) -> str:
        """
        Determine which registered agent should handle the task.

        V1 uses deterministic keyword-based routing.
        Planner is the default fallback.
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

        research_keywords = [
            "riset",
            "research",
            "cari tahu",
            "penelitian",
            "sumber",
            "referensi",
        ]

        if any(keyword in task for keyword in research_keywords):
            return "researcher"

        if any(keyword in task for keyword in planning_keywords):
            return "planner"

        return "planner"
