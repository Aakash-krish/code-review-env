"""
Grader for medium_task: Fix Logic Error.
Evaluates whether the agent correctly fixed a logical error in Python code.
"""

import ast


# Task definition for the medium task
TASK = {
    "id": "medium_task",
    "level": "medium",
    "buggy_code": "def check(x):\n    if x > 10:\n        return 'small'",
    "expected_fix": "def check(x):\n    if x > 10:\n        return 'big'"
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


def grade(*args, **kwargs) -> float:
    """
    Grade the user's fix for the medium logic error task.
    Returns:
        A float score in [0.001, 0.999].
    """
    task = TASK
    user_fix = ""

    # Attempt to extract user_fix flexibly
    if "user_fix" in kwargs:
        user_fix = kwargs["user_fix"]
    elif "fixed_code" in kwargs:
        user_fix = kwargs["fixed_code"]
    elif args and isinstance(args[-1], str):
        user_fix = args[-1]
    
    # Attempt to extract task flexibly if provided
    if "task" in kwargs:
        task = kwargs["task"]
    elif args and isinstance(args[0], dict):
        task = args[0]

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
