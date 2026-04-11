from fastapi import FastAPI
from tasks import get_task, get_task_by_id
from grader import grade
 
app = FastAPI()
 
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
 
@app.get("/state")
def state():
    return current_task