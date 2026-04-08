import requests

BASE_URL = "http://localhost:8000"

# Reset environment
task = requests.get(f"{BASE_URL}/reset").json()
print("Task:", task)

# Dummy fix (just returns expected for demo)
fix = {
    "fixed_code": task["expected_fix"]
}

# Send to environment
result = requests.post(f"{BASE_URL}/step", json=fix).json()
print("Result:", result)