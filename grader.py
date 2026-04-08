def grade(task, user_fix):
    expected = task["expected_fix"]

    # Basic correctness
    if user_fix.strip() == expected.strip():
        return 1.0

    # Partial match
    if expected.split()[0] in user_fix:
        return 0.5

    return 0.0