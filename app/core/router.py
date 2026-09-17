from app.models.state import AIState


class Router:

    def detect_intent(self, task: str) -> str:
        """
        if any(keyword in task for keyword in research_keywords):
            return "research"

        if any(keyword in task for keyword in planning_keywords):
            return "planning"

        if any(keyword in task for keyword in coding_keywords):
            return "coding"

        return "fallback"

        Detect the user's intent using deterministic rules.

        V1 supports:
        - coding
        - research
        - planning
        - fallback
        """
        task = task.lower()

        coding_keywords = [
            "kode",
            "coding",
            "program",
            "programming",
            "buatkan code",
            "buat kode",
            "debug",
            "perbaiki code",
        ]

        research_keywords = [
            "riset",
            "research",
            "cari tahu",
            "penelitian",
            "sumber",
            "referensi",
        ]

        planning_keywords = [
            "rencana",
            "planning",
            "plan",
            "langkah",
            "strategi",
            "belajar",
        ]

        if any(keyword in task for keyword in coding_keywords):
            return "coding"

        if any(keyword in task for keyword in research_keywords):
            return "research"

        if any(keyword in task for keyword in planning_keywords):
            return "planning"

        return "fallback"

    def route(self, state: AIState) -> str:
        """
        Map detected intent to a registered agent.
        """
        intent = self.detect_intent(state.get("task", ""))

        if intent == "coding":
            return "coder"

        if intent == "research":
            return "researcher"

        if intent == "planning":
            return "planner"

        return "planner"
