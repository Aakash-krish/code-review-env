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

BASE_URL = "http://localhost:8000"

# START
print("START")

task = requests.get(f"{BASE_URL}/reset").json()
print(task)

# STEP
print("STEP")

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": f"Fix this code:\n{task['buggy_code']}"}
    ]
)

fix = {
    "fixed_code": response.choices[0].message.content
}

print(fix)

result = requests.post(f"{BASE_URL}/step", json=fix).json()

# END
print("END")
print(result)