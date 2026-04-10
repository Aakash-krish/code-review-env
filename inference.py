from openai import OpenAI
import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")

# -------- START --------
try:
    task = requests.post(f"{BASE_URL}/reset").json()
except:
    task = {"buggy_code": "print('hello')"}

print(f"[START] task=code_review", flush=True)

# -------- STEP --------
buggy_code = task.get("buggy_code", "")

prompt = f"""Fix this Python code. Return only code.

{buggy_code}
"""

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    fixed_code = response.choices[0].message.content.strip()
except:
    fixed_code = buggy_code

fix = {"fixed_code": fixed_code}

try:
    result = requests.post(f"{BASE_URL}/step", json=fix).json()
    score = result.get("score", 0.0)
except:
    score = 0.0

print(f"[STEP] step=1 reward={score}", flush=True)

# -------- END --------
print(f"[END] task=code_review score={score} steps=1", flush=True)