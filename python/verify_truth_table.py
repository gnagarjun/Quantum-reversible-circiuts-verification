"""
verify_truth_table.py
Verifies the sigma3 gate truth table against expected values.
"""

# Expected truth table for sigma3:
# (I1, I2, S) -> (O1, O2, S_out)
# S=0: swap  -> O1=I2, O2=I1
# S=1: pass  -> O1=I1, O2=I2
EXPECTED_TRUTH_TABLE = {
    (0, 0, 0): (0, 0, 0),
    (0, 1, 0): (1, 0, 0),
    (1, 0, 0): (0, 1, 0),
    (1, 1, 0): (1, 1, 0),
    (0, 0, 1): (0, 0, 1),
    (0, 1, 1): (0, 1, 1),
    (1, 0, 1): (1, 0, 1),
    (1, 1, 1): (1, 1, 1),
}


def verify_truth_table(sigma3_results):
    """
    Compare simulation sigma3 results against expected truth table.
    Returns dict with status (PASS/FAIL) and details.
    """
    errors = []
    checked = 0

    for row in sigma3_results:
        key = (row["I1"], row["I2"], row["S"])
        expected = EXPECTED_TRUTH_TABLE.get(key)
        if expected is None:
            errors.append(f"Unexpected input combination: {key}")
            continue
        actual = (row["O1"], row["O2"], row["S_out"])
        if actual != expected:
            errors.append(
                f"Input {key}: expected output {expected}, got {actual}"
            )
        checked += 1

    # Check all 8 entries were tested
    missing = set(EXPECTED_TRUTH_TABLE.keys()) - {
        (r["I1"], r["I2"], r["S"]) for r in sigma3_results
    }
    for m in missing:
        errors.append(f"Missing input combination: {m}")

    status = "PASS" if not errors else "FAIL"
    return {
        "verification": "Truth Table",
        "status": status,
        "checked": checked,
        "errors": errors,
    }


if __name__ == "__main__":
    import json
    import sys
    sys.path.insert(0, ".")
    from parse_output import parse_log
    data = parse_log()
    result = verify_truth_table(data["sigma3"])
    print(json.dumps(result, indent=2))

