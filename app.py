from fastapi import FastAPI
from tasks import get_task
from grader import grade

app = FastAPI()

current_task = {}

@app.get("/")
def home():
    return {"message": "Code Review Environment Running 🚀"}

# ✅ REQUIRED: POST /reset
@app.post("/reset")
def reset():
    global current_task
    current_task = get_task()
    return current_task

# ✅ REQUIRED: POST /step
@app.post("/step")
def step(action: dict):
    global current_task
    
    user_fix = action.get("fixed_code", "")
    score = grade(current_task, user_fix)

    done = True if score > 0.8 else False

    return {
        "score": score,
        "done": done
    }

# ✅ REQUIRED: GET /state
@app.get("/state")
def state():
    return current_task