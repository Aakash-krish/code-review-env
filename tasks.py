tasks = [
    {
        "id": "easy_task",
        "level": "easy",
        "buggy_code": "print('Hello World'",
        "expected_fix": "print('Hello World')"
    },
    {
        "id": "medium_task",
        "level": "medium",
        "buggy_code": "def check(x):\n    if x > 10:\n        return 'small'",
        "expected_fix": "def check(x):\n    if x > 10:\n        return 'big'"
    },
    {
        "id": "hard_task",
        "level": "hard",
        "buggy_code": "def find_max(arr):\n    max = 0\n    for i in arr:\n        if i > max:\n            max = i\n    return max",
        "expected_fix": "def find_max(arr):\n    max_val = arr[0]\n    for i in arr:\n        if i > max_val:\n            max_val = i\n    return max_val"
    }
]

task_index = 0

def get_task():
    global task_index
    task = tasks[task_index]
    task_index = (task_index + 1) % len(tasks)
    return task