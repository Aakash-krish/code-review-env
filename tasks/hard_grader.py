"""
Grader for hard_task: Fix Complex Bug.
Evaluates whether the agent correctly fixed a complex bug involving
shadowed builtins and edge case failures.
"""

import ast


# Task definition for the hard task
TASK = {
    "id": "hard_task",
    "level": "hard",
    "buggy_code": (
        "def find_max(arr):\n"
        "    max = 0\n"
        "    for i in arr:\n"
        "        if i > max:\n"
        "            max = i\n"
        "    return max"
    ),
    "expected_fix": (
        "def find_max(arr):\n"
        "    max_val = arr[0]\n"
        "    for i in arr:\n"
        "        if i > max_val:\n"
        "            max_val = i\n"
        "    return max_val"
    )
}


def _strip_code_fences(code: str) -> str:
    """Remove markdown code fences if present."""
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        if lines[-1].strip() == "```":
            code = "\n".join(lines[1:-1])
        else:
            code = "\n".join(lines[1:])
        code = code.strip()
    return code


def grade(task: dict = None, user_fix: str = "") -> float:
    """
    Grade the user's fix for the hard complex bug task.

    Args:
        task: Optional task dict. If None, uses the built-in TASK.
        user_fix: The user's proposed fix as a string.

    Returns:
        A float score in [0.001, 0.999].
    """
    if task is None:
        task = TASK

    if not user_fix:
        return 0.001

    expected = task.get("expected_fix", TASK["expected_fix"]).strip()
    user_fix = _strip_code_fences(user_fix.strip())

    # 1. Exact match
    if user_fix == expected:
        return 0.999

    # 2. Whitespace-normalized match
    if " ".join(user_fix.split()) == " ".join(expected.split()):
        return 0.999

    # 3. AST-based comparison (functionally equivalent code)
    try:
        expected_ast = ast.dump(ast.parse(expected))
        user_ast = ast.dump(ast.parse(user_fix))
        if expected_ast == user_ast:
            return 0.999
    except SyntaxError:
        pass

    # 4. Partial match: check key token overlap
    expected_tokens = set(expected.split())
    user_tokens = set(user_fix.split())
    overlap = len(expected_tokens & user_tokens) / max(len(expected_tokens), 1)

    if overlap >= 0.85:
        return 0.9
    elif overlap >= 0.6:
        return 0.5
    elif overlap >= 0.3:
        return 0.3

    return 0.001
