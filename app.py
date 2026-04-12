from fastapi import FastAPI
from tasks import get_task, get_task_by_id
from grader import grade
from tasks import easy_grader, medium_grader, hard_grader
 
app = FastAPI()
 
# Map task IDs to their specific grader modules
GRADERS = {
    "easy_task": easy_grader,
    "medium_task": medium_grader,
    "hard_task": hard_grader,
}
 
current_task = None
 
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
    score = grade(current_task, user_fix)
 
    return {
        "score": score,
        "done": True,
        "info": {
            "task_id": current_task["id"],
            "level": current_task["level"]
        }
    }
 
@app.post("/grade/{task_id}")
def grade_task(task_id: str, action: dict):
    """Grade a specific task by ID using its dedicated grader module."""
    grader_module = GRADERS.get(task_id)
    if grader_module is None:
        return {"error": f"Unknown task_id: {task_id}", "score": 0.001}
 
    user_fix = action.get("fixed_code", "")
    score = grader_module.grade(user_fix=user_fix)
 
    return {
        "task_id": task_id,
        "score": score,
        "done": True,
    }
 
@app.get("/state")
def state():
    return current_task