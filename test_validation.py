"""Verification test for hackathon Phase 2 validation fix."""

import yaml
import sys

print("=" * 50)
print("VERIFICATION TESTS")
print("=" * 50)

# Test 1: Parse openenv.yaml and verify tasks
with open("openenv.yaml", "r") as f:
    config = yaml.safe_load(f)

tasks = config.get("tasks", [])
print(f"\n[TEST 1] Tasks found in openenv.yaml: {len(tasks)}")
for t in tasks:
    print(f"  - id={t['id']}, grader={t['grader']}, difficulty={t['difficulty']}")

assert len(tasks) >= 3, f"FAIL: Only {len(tasks)} tasks, need >= 3"
print("[TEST 1] PASSED: 3+ tasks with graders\n")

# Test 2: Import each grader module
from tasks.easy_grader import grade as easy_grade
from tasks.medium_grader import grade as medium_grade
from tasks.hard_grader import grade as hard_grade
print("[TEST 2] PASSED: All grader modules imported successfully\n")

# Test 3: Test grader outputs are in (0, 1)
score1 = easy_grade(user_fix="print('Hello World')")
print(f"[TEST 3a] easy_grade(correct) = {score1}")
assert 0 < score1 < 1, f"FAIL: score {score1} not in (0,1)"

score2 = medium_grade(user_fix="def check(x):\n    if x > 10:\n        return 'big'")
print(f"[TEST 3b] medium_grade(correct) = {score2}")
assert 0 < score2 < 1, f"FAIL: score {score2} not in (0,1)"

score3 = hard_grade(
    user_fix=(
        "def find_max(arr):\n"
        "    max_val = arr[0]\n"
        "    for i in arr:\n"
        "        if i > max_val:\n"
        "            max_val = i\n"
        "    return max_val"
    )
)
print(f"[TEST 3c] hard_grade(correct) = {score3}")
assert 0 < score3 < 1, f"FAIL: score {score3} not in (0,1)"

# Test wrong answer
score4 = easy_grade(user_fix="totally wrong code")
print(f"[TEST 3d] easy_grade(wrong) = {score4}")
assert 0 < score4 < 1, f"FAIL: score {score4} not in (0,1)"

# Test empty answer
score5 = easy_grade(user_fix="")
print(f"[TEST 3e] easy_grade(empty) = {score5}")
assert 0 < score5 < 1, f"FAIL: score {score5} not in (0,1)"

print("[TEST 3] PASSED: All grader scores are strictly in (0, 1)\n")

# Test 4: Verify grader paths resolve correctly
for t in tasks:
    grader_path = t["grader"]
    module_path, func_name = grader_path.split(":")
    mod = __import__(module_path, fromlist=[func_name])
    func = getattr(mod, func_name)
    assert callable(func), f"FAIL: {grader_path} is not callable"
    print(f"[TEST 4] {grader_path} -> {func} (callable)")

print("[TEST 4] PASSED: All grader paths resolve to callable functions\n")

print("=" * 50)
print("ALL TESTS PASSED - Ready to submit!")
print("=" * 50)
