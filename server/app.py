from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from tasks import get_task, get_task_by_id
from tasks.easy_grader import grade as easy_grade
from tasks.medium_grader import grade as medium_grade
from tasks.hard_grader import grade as hard_grade
import os

app = FastAPI(title="code-review-env", version="1.0.0")

GRADERS = {
    "easy_task": easy_grade,
    "medium_task": medium_grade,
    "hard_task": hard_grade,
}

current_task = None

OPENENV_YAML_PATH = os.path.join(os.path.dirname(__file__), "..", "openenv.yaml")

# ── Required by openenv validator ───────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metadata")
def metadata():
    return {
        "name": "code-review-env",
        "description": "AI agent environment for code review and bug fixing. Supports easy, medium, and hard Python debugging tasks.",
        "version": "1.0.0"
    }

@app.get("/schema")
def schema():
    return {
        "action": {"fixed_code": "string"},
        "observation": {"buggy_code": "string", "task_id": "string", "level": "string"},
        "state": {"task_id": "string", "level": "string", "buggy_code": "string"}
    }

@app.post("/mcp")
async def mcp(request: Request):
    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    return {
        "jsonrpc": "2.0",
        "id": body.get("id", 1),
        "result": {"tools": []}
    }

@app.get("/tasks")
def list_tasks():
    import yaml
    with open(OPENENV_YAML_PATH, "r") as f:
        config = yaml.safe_load(f)
    return {"tasks": config.get("tasks", [])}

@app.get("/openenv.yaml", response_class=PlainTextResponse)
def serve_openenv_yaml():
    with open(OPENENV_YAML_PATH, "r") as f:
        return f.read()

# ── Standard endpoints ───────────────────────────────────────────────────────

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
    if current_task is None:
        return {"error": "No active task"}
    return {
        "task_id": current_task["id"],
        "level": current_task["level"],
        "buggy_code": current_task["buggy_code"]
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()