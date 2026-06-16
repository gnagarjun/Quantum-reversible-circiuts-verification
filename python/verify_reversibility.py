"""
verify_reversibility.py
Verifies that the sigma3 gate is reversible (bijective mapping).
"""


def verify_reversibility(sigma3_results):
    """
    A reversible gate must have a bijection between inputs and outputs.
    Every input must map to a unique output (no two inputs share the same output).
    """
    input_output_map = {}
    output_set = set()
    collisions = []

    for row in sigma3_results:
        inp = (row["I1"], row["I2"], row["S"])
        out = (row["O1"], row["O2"], row["S_out"])
        input_output_map[inp] = out
        if out in output_set:
            collisions.append(f"Collision: multiple inputs map to output {out}")
        output_set.add(out)

    num_inputs = len(input_output_map)
    num_unique_outputs = len(output_set)

    details = {
        "num_inputs": num_inputs,
        "num_unique_outputs": num_unique_outputs,
        "bijection": num_inputs == num_unique_outputs,
        "mapping": {str(k): str(v) for k, v in input_output_map.items()},
        "collisions": collisions,
    }

    status = "PASS" if details["bijection"] and not collisions else "FAIL"
    return {
        "verification": "Reversibility",
        "status": status,
        "details": details,
    }


if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, ".")
    from parse_output import parse_log
    data = parse_log()
    result = verify_reversibility(data["sigma3"])
    print(json.dumps(result, indent=2))

