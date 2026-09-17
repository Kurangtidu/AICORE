from app.core.router import Router


def test_router_planning_task():
    router = Router()

    state = {
        "task": "Buat rencana belajar Python",
    }

    assert router.route(state) == "planner"


def test_router_fallback():
    router = Router()

    state = {
        "task": "Halo, apa kabar?",
    }

    assert router.route(state) == "planner"

def test_router_research_task():
    router = Router()

    state = {
        "task": "Riset tentang LangGraph",
    }

    assert router.route(state) == "researcher"
