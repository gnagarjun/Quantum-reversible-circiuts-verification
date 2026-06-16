"""
verify_aes_field_ops.py
Verifies AES GF(2^8) field arithmetic (Paper Slides 8, 11, 12).

Slide 11 — Circuit Addition: add_polynomials(r,w) = [r1 XOR w1, ..., r8 XOR w8]
Slide 12 — Circuit Multiplication: GF(2^8) mul mod m(x)
Slide 8  — Example: p(x)=x^6+x^4+x (0x52), q(x)=x^2+1 (0x05), p*q mod m = 1
"""


# ── GF(2^8) reference implementation ──────────────────────────────────────────

def gf_mul_ref(a: int, b: int) -> int:
    """Software reference GF(2^8) multiply mod m(x)=x^8+x^4+x^3+x+1."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


# ── Slide 11: Field Addition ───────────────────────────────────────────────────

def verify_aes_field_add(fadd_results):
    """
    GF(2^8) addition = bitwise XOR.
    Verify simulation results match expected XOR for each test case.
    """
    errors = []
    for row in fadd_results:
        expected = row["r"] ^ row["w"]
        if row["sum"] != expected:
            errors.append(
                f"FADD(0x{row['r']:02X}, 0x{row['w']:02X}): "
                f"expected 0x{expected:02X}, got 0x{row['sum']:02X}"
            )

    # Algebraic properties verified in Python
    prop_errors = []
    for a, b in [(0x52, 0x05), (0xAB, 0xCD), (0xFF, 0x00)]:
        if (a ^ b) != (b ^ a):
            prop_errors.append(f"Commutativity failed: 0x{a:02X}+0x{b:02X}")
    for a in [0x52, 0xAB, 0xFF]:
        if (a ^ 0) != a:
            prop_errors.append(f"Identity failed: 0x{a:02X}+0 != 0x{a:02X}")
    for a in [0x52, 0xAB, 0xFF]:
        if (a ^ a) != 0:
            prop_errors.append(f"Self-inverse failed: 0x{a:02X}+0x{a:02X} != 0")

    status = "PASS" if not errors and not prop_errors else "FAIL"
    return {
        "verification": "AES GF(2^8) Field Addition — Slide 11",
        "status": status,
        "description": "add_polynomials(r,w) = bitwise XOR of 8 coefficient bits",
        "errors": errors + prop_errors,
    }


# ── Slide 12 + Slide 8: Field Multiplication ──────────────────────────────────

def verify_aes_field_mul(fmul_results):
    """
    Verify GF(2^8) multiplication results from simulation.
    Key test: paper example p(x)=0x52, q(x)=0x05 -> product=0x01.
    """
    errors = []
    for row in fmul_results:
        expected = gf_mul_ref(row["a"], row["b"])
        if row["product"] != expected:
            errors.append(
                f"FMUL(0x{row['a']:02X}, 0x{row['b']:02X}): "
                f"expected 0x{expected:02X}, got 0x{row['product']:02X}"
            )

    # Paper's specific example from Slide 8
    paper_example_result = gf_mul_ref(0x52, 0x05)
    paper_ok = paper_example_result == 0x01
    if not paper_ok:
        errors.append(
            f"Paper example FAILED: 0x52 x 0x05 mod m(x) = "
            f"0x{paper_example_result:02X}, expected 0x01"
        )

    # Algebraic properties
    prop_errors = []
    for a in [0x52, 0xAB, 0x01, 0xFF]:
        if gf_mul_ref(a, 0x01) != a:
            prop_errors.append(f"Identity failed: 0x{a:02X} * 1 != 0x{a:02X}")
    for a in [0x52, 0xAB, 0xFF]:
        if gf_mul_ref(a, 0x00) != 0:
            prop_errors.append(f"Zero failed: 0x{a:02X} * 0 != 0")
    for a, b in [(0x53, 0xCA), (0x52, 0x05), (0x0F, 0xF0)]:
        if gf_mul_ref(a, b) != gf_mul_ref(b, a):
            prop_errors.append(f"Commutativity failed: 0x{a:02X}*0x{b:02X}")
    for a, b, c in [(0x53, 0x05, 0x10)]:
        if gf_mul_ref(a, b ^ c) != (gf_mul_ref(a, b) ^ gf_mul_ref(a, c)):
            prop_errors.append(f"Distributivity failed for a=0x{a:02X}")

    status = "PASS" if not errors and not prop_errors else "FAIL"
    return {
        "verification": "AES GF(2^8) Field Multiplication — Slides 8 & 12",
        "status": status,
        "paper_example": {
            "p_x": "x^6+x^4+x (0x52)",
            "q_x": "x^2+1 (0x05)",
            "result": f"0x{paper_example_result:02X}",
            "expected": "0x01 (multiplicative inverses)",
            "passed": paper_ok,
        },
        "irreducible_polynomial": "m(x) = x^8+x^4+x^3+x+1",
        "errors": errors + prop_errors,
    }


# ── Slide 9: Lookup Table Memory Complexity ────────────────────────────────────

def verify_lookup_table_complexity():
    """
    Verify paper's claim: n * 2^n bits needed for an n-input truth table.
    n=32 -> 137,438,953,472 bits
    n=64 -> 1,180,591,620,717,411,303,424 bits
    """
    errors = []
    n32_expected = 32 * (2 ** 32)
    n64_expected = 64 * (2 ** 64)
    n32_paper = 137_438_953_472
    n64_paper = 1_180_591_620_717_411_303_424

    if n32_expected != n32_paper:
        errors.append(f"n=32: calculated {n32_expected}, paper says {n32_paper}")
    if n64_expected != n64_paper:
        errors.append(f"n=64: calculated {n64_expected}, paper says {n64_paper}")

    return {
        "verification": "Lookup Table Memory Complexity — Slide 9",
        "status": "PASS" if not errors else "FAIL",
        "formula": "n x 2^n bits",
        "n32_bits": n32_expected,
        "n64_bits": n64_expected,
        "errors": errors,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(verify_lookup_table_complexity(), indent=2))

