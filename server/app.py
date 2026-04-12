from fastapi import FastAPI
from tasks import get_task, get_task_by_id
from tasks.easy_grader import grade as easy_grade
from tasks.medium_grader import grade as medium_grade
from tasks.hard_grader import grade as hard_grade

app = FastAPI()

GRADERS = {
    "easy_task": easy_grade,
    "medium_task": medium_grade,
    "hard_task": hard_grade,
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