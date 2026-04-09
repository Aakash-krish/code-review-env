from openai import OpenAI
import os
import requests
 
# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
 
# OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)
 
# Fix 1: Use port 7860 to match the server, and allow override via env
BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")
 
# START
print("START")
 
# Fix 2: /reset is a POST endpoint, not GET
task = requests.post(f"{BASE_URL}/reset").json()
print(task)
 
# STEP
print("STEP")
 
buggy_code = task.get("buggy_code", "")
level = task.get("level", "easy")
 
prompt = f"""You are a code debugging assistant. Fix the following buggy Python code.
Return ONLY the fixed code with no explanation, no markdown, no code fences.
Just the raw fixed Python code.
 
Buggy code:
{buggy_code}"""
 
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": prompt}
    ]
)
 
fixed_code = response.choices[0].message.content.strip()
 
# Strip markdown code fences if the model adds them anyway
if fixed_code.startswith("```"):
    lines = fixed_code.split("\n")
    # Remove first and last fence lines
    fixed_code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
 
print("Fixed code:", fixed_code)
 
fix = {"fixed_code": fixed_code}
 
result = requests.post(f"{BASE_URL}/step", json=fix).json()
 
# END
print("END")
print(result)