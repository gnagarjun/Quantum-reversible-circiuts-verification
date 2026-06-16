"""
verify_xor_circuit.py
Verifies XOR circuit (Paper Slide 10): A XOR B = (A OR B) AND NOT(A AND B)
Checks simulation output against expected XOR truth table.
"""

EXPECTED_XOR = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}


def verify_xor_circuit(xor_results):
    errors = []
    for row in xor_results:
        key = (row["A"], row["B"])
        expected = EXPECTED_XOR.get(key)
        if row["XOR_OUT"] != expected:
            errors.append(
                f"XOR({key[0]},{key[1]}): expected {expected}, got {row['XOR_OUT']}"
            )
    # Also verify the formula: A XOR B = (A OR B) AND NOT(A AND B)
    for (a, b), expected in EXPECTED_XOR.items():
        formula_val = int(bool((a | b) & (not (a & b))))
        if formula_val != expected:
            errors.append(
                f"Formula check failed for A={a},B={b}: got {formula_val}, expected {expected}"
            )
    status = "PASS" if not errors else "FAIL"
    return {
        "verification": "XOR Circuit from sigma3 (Slide 10)",
        "status": status,
        "formula": "A XOR B = (A OR B) AND NOT(A AND B)",
        "errors": errors,
    }


if __name__ == "__main__":
    import json
    sample = [
        {"A": 0, "B": 0, "XOR_OUT": 0},
        {"A": 0, "B": 1, "XOR_OUT": 1},
        {"A": 1, "B": 0, "XOR_OUT": 1},
        {"A": 1, "B": 1, "XOR_OUT": 0},
    ]
    print(json.dumps(verify_xor_circuit(sample), indent=2))

