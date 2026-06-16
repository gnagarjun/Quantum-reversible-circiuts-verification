"""
verify_self_modifiable.py
Verifies the self-modifiable circuit behavior:
  S=0: O4=NAND(I1,I2), O2=NOR(I1,I2)
  S=1: O4=NOR(I1,I2),  O2=NAND(I1,I2)
"""


def nand(a, b):
    return int(not (a and b))


def nor(a, b):
    return int(not (a or b))


def verify_self_modifiable(selfmod_results):
    errors = []

    for row in selfmod_results:
        I1, I2, S = row["I1"], row["I2"], row["S"]
        O2, O4 = row["O2"], row["O4"]

        expected_nand = nand(I1, I2)
        expected_nor = nor(I1, I2)

        if S == 0:
            # O4 = NAND, O2 = NOR
            if O4 != expected_nand:
                errors.append(
                    f"S=0, I1={I1}, I2={I2}: O4 expected NAND={expected_nand}, got {O4}"
                )
            if O2 != expected_nor:
                errors.append(
                    f"S=0, I1={I1}, I2={I2}: O2 expected NOR={expected_nor}, got {O2}"
                )
        else:
            # S=1: O4 = NOR, O2 = NAND
            if O4 != expected_nor:
                errors.append(
                    f"S=1, I1={I1}, I2={I2}: O4 expected NOR={expected_nor}, got {O4}"
                )
            if O2 != expected_nand:
                errors.append(
                    f"S=1, I1={I1}, I2={I2}: O2 expected NAND={expected_nand}, got {O2}"
                )

    status = "PASS" if not errors else "FAIL"
    return {
        "verification": "Self-Modifiable Circuit",
        "status": status,
        "tested_rows": len(selfmod_results),
        "errors": errors,
    }


if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, ".")
    from parse_output import parse_log
    data = parse_log()
    result = verify_self_modifiable(data["selfmod"])
    print(json.dumps(result, indent=2))

