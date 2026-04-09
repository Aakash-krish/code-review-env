import ast
 
def grade(task, user_fix):
    expected = task["expected_fix"].strip()
    user_fix = user_fix.strip()
 
    # Strip markdown code fences if present
    if user_fix.startswith("```"):
        lines = user_fix.split("\n")
        user_fix = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
        user_fix = user_fix.strip()
 
    # 1. Exact match → full score
    if user_fix == expected:
        return 1.0
 
    # 2. Normalize whitespace and compare
    if " ".join(user_fix.split()) == " ".join(expected.split()):
        return 1.0
 
    # 3. AST-based comparison (functionally equivalent code)
    try:
        expected_ast = ast.dump(ast.parse(expected))
        user_ast = ast.dump(ast.parse(user_fix))
        if expected_ast == user_ast:
            return 1.0
    except SyntaxError:
        pass
 
    # 4. Partial match: check key tokens from expected are present
    expected_tokens = set(expected.split())
    user_tokens = set(user_fix.split())
    overlap = len(expected_tokens & user_tokens) / max(len(expected_tokens), 1)
 
    if overlap >= 0.85:
        return 0.9
    elif overlap >= 0.6:
        return 0.5
    elif overlap >= 0.3:
        return 0.3
 
    return 0.0