from fastapi import FastAPI
from tasks import get_task
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
    return current_task

@app.post("/step")
def step(action: dict):
    global current_task

    user_fix = action.get("fixed_code", "")
    score = grade(current_task, user_fix)

    return {
        "score": score,
        "done": True,  # ✅ always true
        "info": {
            "task_id": current_task.get("id"),
            "level": current_task.get("level")
        }
    }

@app.get("/state")
def state():
    return current_task