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

# ✅ Correct port (7860)
BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")

# ---------------- START ----------------
print("START")

try:
    task = requests.post(f"{BASE_URL}/reset").json()
except Exception as e:
    task = {"buggy_code": "print('hello world')"}  # fallback

print(task)

# ---------------- STEP ----------------
print("STEP")

buggy_code = task.get("buggy_code", "")

prompt = f"""You are a code debugging assistant. Fix the following buggy Python code.
Return ONLY the fixed code. No explanation.

Buggy code:
{buggy_code}
"""

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    fixed_code = response.choices[0].message.content.strip()

except Exception as e:
    # ✅ fallback if API fails
    fixed_code = buggy_code

# Remove markdown fences if any
if fixed_code.startswith("```"):
    lines = fixed_code.split("\n")
    fixed_code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

fix = {"fixed_code": fixed_code}

print(fix)

# ---------------- END ----------------
try:
    result = requests.post(f"{BASE_URL}/step", json=fix).json()
except Exception as e:
    result = {"score": 0.0, "done": False}

print("END")
print(result)