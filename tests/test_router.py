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

def test_router_detect_intent():
    router = Router()

    assert router.detect_intent("Buat rencana belajar Python") == "planning"
    assert router.detect_intent("Riset tentang LangGraph") == "research"
    assert router.detect_intent("Halo, apa kabar?") == "fallback"
