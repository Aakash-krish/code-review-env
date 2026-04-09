from fastapi import FastAPI
from tasks import get_task
from grader import grade
 
app = FastAPI()
 
current_task = {}
 
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
    return {"score": score, "done": score > 0.8}
 
@app.get("/state")
def state():
    return current_task