from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from tasks import get_task, get_task_by_id
from tasks.easy_grader import grade as easy_grade
from tasks.medium_grader import grade as medium_grade
from tasks.hard_grader import grade as hard_grade
import os

app = FastAPI()

GRADERS = {
    "easy_task": easy_grade,
    "medium_task": medium_grade,
    "hard_task": hard_grade,
}

current_task = None

OPENENV_YAML_PATH = os.path.join(os.path.dirname(__file__), "..", "openenv.yaml")

# ── /tasks ── The validator hits this to count tasks with graders ──────────
@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "id": "easy_task",
                "name": "Fix Syntax Error",
                "difficulty": "easy",
                "grader": "tasks.easy_grader:grade",
                "description": "Fix a basic Python syntax error such as a missing bracket."
            },
            {
                "id": "medium_task",
                "name": "Fix Logic Error",
                "difficulty": "medium",
                "grader": "tasks.medium_grader:grade",
                "description": "Fix a logical error such as a wrong return value."
            },
            {
                "id": "hard_task",
                "name": "Fix Complex Bug",
                "difficulty": "hard",
                "grader": "tasks.hard_grader:grade",
                "description": "Fix a complex bug such as a shadowed builtin or edge case failure."
            }
        ]
    }

# ── /openenv.yaml ── serve raw config file ─────────────────────────────────
@app.get("/openenv.yaml", response_class=PlainTextResponse)
def serve_openenv_yaml():
    with open(OPENENV_YAML_PATH, "r") as f:
        return f.read()

# ── /health ─────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}

# ── standard endpoints ───────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset():
    global current_task
    current_task = get_task()
    return {
        "task_id": current_task["id"],
        "level": current_task["level"],
        "buggy_code": current_task["buggy_code"]
    }

@app.post("/reset/{task_id}")
def reset_by_id(task_id: str):
    global current_task
    current_task = get_task_by_id(task_id)
    return {
        "task_id": current_task["id"],
        "level": current_task["level"],
        "buggy_code": current_task["buggy_code"]
    }

@app.post("/step")
def step(action: dict):
    global current_task
    if current_task is None:
        return {"error": "No active task. Call /reset first.", "score": 0.0, "done": False}
    user_fix = action.get("fixed_code", "")
    grader = GRADERS.get(current_task["id"])
    score = grader(user_fix=user_fix) if grader else 0.001
    return {
        "score": score,
        "done": True,
        "info": {"task_id": current_task["id"], "level": current_task["level"]}
    }

@app.post("/grade/{task_id}")
def grade_task(task_id: str, action: dict):
    grader = GRADERS.get(task_id)
    if grader is None:
        return {"error": f"Unknown task_id: {task_id}", "score": 0.001}
    score = grader(user_fix=action.get("fixed_code", ""))
    return {"task_id": task_id, "score": score, "done": True}

@app.get("/state")
def state():
    return current_task

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()