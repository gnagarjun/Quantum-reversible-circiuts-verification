"""
verify_obfuscation.py
Verifies circuit obfuscation behavior from Paper Slides 13 & 14.

Slide 14 — Random XOR Circuit:
  b=1: z = x XOR y,  w = x
  b=0: z = x,        w = x XOR y

Slide 13 — Circuit Obfuscation:
  b=1: u=p4,      v=p4 XOR p1,  w=p5,         z=p5 XOR p1
  b=0: u=p5 XOR p1, v=p5,       w=p4 XOR p1,  z=p4
"""


def verify_random_xor(oxor_results):
    """
    Slide 14: Verify the obfuscated XOR circuit.
    The XOR result moves between output locations based on b.
    """
    errors = []
    for row in oxor_results:
        x, y, b = row["x"], row["y"], row["b"]
        z, w = row["z"], row["w"]
        xor_val = x ^ y

        if b == 1:
            if z != xor_val:
                errors.append(
                    f"b=1, x={x},y={y}: z expected {xor_val} (x XOR y), got {z}"
                )
            if w != x:
                errors.append(f"b=1, x={x},y={y}: w expected {x} (x), got {w}")
        else:
            if z != x:
                errors.append(f"b=0, x={x},y={y}: z expected {x} (x), got {z}")
            if w != xor_val:
                errors.append(
                    f"b=0, x={x},y={y}: w expected {xor_val} (x XOR y), got {w}"
                )

    status = "PASS" if not errors else "FAIL"
    return {
        "verification": "Random XOR Circuit (Moving Computation) — Slide 14",
        "status": status,
        "description": (
            "b=1: z=x XOR y, w=x | b=0: z=x, w=x XOR y — "
            "XOR result moves location without changing wiring"
        ),
        "errors": errors,
    }


def verify_circuit_obfuscation(cobf_results):
    """
    Slide 13: Verify polynomial coefficient routing via sigma3.
    b=1: u=p4,       v=p4 XOR p1, w=p5,        z=p5 XOR p1
    b=0: u=p5 XOR p1, v=p5,       w=p4 XOR p1, z=p4
    """
    errors = []
    for row in cobf_results:
        p1 = row["p1"]; p4 = row["p4"]; p5 = row["p5"]; b = row["b"]
        u = row["u"]; v = row["v"]; w = row["w"]; z = row["z"]

        xor_p4_p1 = p4 ^ p1
        xor_p5_p1 = p5 ^ p1

        if b == 1:
            if u != p4:
                errors.append(
                    f"b=1 p1={p1},p4={p4},p5={p5}: u expected p4={p4}, got {u}"
                )
            if v != xor_p4_p1:
                errors.append(
                    f"b=1 p1={p1},p4={p4},p5={p5}: v expected p4 XOR p1={xor_p4_p1}, got {v}"
                )
            if w != p5:
                errors.append(
                    f"b=1 p1={p1},p4={p4},p5={p5}: w expected p5={p5}, got {w}"
                )
            if z != xor_p5_p1:
                errors.append(
                    f"b=1 p1={p1},p4={p4},p5={p5}: z expected p5 XOR p1={xor_p5_p1}, got {z}"
                )
        else:
            if u != xor_p5_p1:
                errors.append(
                    f"b=0 p1={p1},p4={p4},p5={p5}: u expected p5 XOR p1={xor_p5_p1}, got {u}"
                )
            if v != p5:
                errors.append(
                    f"b=0 p1={p1},p4={p4},p5={p5}: v expected p5={p5}, got {v}"
                )
            if w != xor_p4_p1:
                errors.append(
                    f"b=0 p1={p1},p4={p4},p5={p5}: w expected p4 XOR p1={xor_p4_p1}, got {w}"
                )
            if z != p4:
                errors.append(
                    f"b=0 p1={p1},p4={p4},p5={p5}: z expected p4={p4}, got {z}"
                )

    status = "PASS" if not errors else "FAIL"
    return {
        "verification": "Circuit Obfuscation (Polynomial Routing) — Slide 13",
        "status": status,
        "description": (
            "sigma3 routes p4/p5 group values to different locations based on b, "
            "implementing 'moving computation' without rewiring"
        ),
        "errors": errors,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(verify_random_xor([]), indent=2))
    print(json.dumps(verify_circuit_obfuscation([]), indent=2))

