"""
generate_report.py
Main entry point: runs ALL simulations, verifies every claim from the
research paper, generates JSON report and optional PDF.
"""

import json
import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_DIR = os.path.join(BASE_DIR, "python")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
sys.path.insert(0, PYTHON_DIR)

from run_simulation import (
    compile_verilog, compile_aes_verilog,
    run_simulation, run_aes_simulation,
    AES_SIM_LOG,
)
from parse_output import parse_log
from verify_truth_table import verify_truth_table
from verify_reversibility import verify_reversibility
from verify_self_modifiable import verify_self_modifiable
from verify_xor_circuit import verify_xor_circuit
from verify_aes_field_ops import (
    verify_aes_field_add,
    verify_aes_field_mul,
    verify_lookup_table_complexity,
)
from verify_obfuscation import verify_random_xor, verify_circuit_obfuscation
from verify_sbox_complexity import (
    verify_sbox_complexity,
    verify_non_one_way_function_claim,
    verify_side_channel_resistance,
    verify_general_method,
    verify_xor_gate_cost,
    verify_permutation_complexity,
    verify_kerckhoffs_principle,
    verify_quantum_applicability,
    verify_heisenberg_obfuscation,
    verify_circuit_repair_potential,
)


def verify_nand(nand_results):
    EXPECTED = {(0,0):1,(0,1):1,(1,0):1,(1,1):0}
    errors = []
    for row in nand_results:
        key = (row["A"], row["B"])
        if row["NAND_OUT"] != EXPECTED.get(key):
            errors.append(f"NAND({key}): expected {EXPECTED[key]}, got {row['NAND_OUT']}")
    return {"verification": "NAND from σ3 (Slide 4/Roadmap)", "status": "PASS" if not errors else "FAIL", "errors": errors}


def verify_nor(nor_results):
    EXPECTED = {(0,0):1,(0,1):0,(1,0):0,(1,1):0}
    errors = []
    for row in nor_results:
        key = (row["A"], row["B"])
        if row["NOR_OUT"] != EXPECTED.get(key):
            errors.append(f"NOR({key}): expected {EXPECTED[key]}, got {row['NOR_OUT']}")
    return {"verification": "NOR from σ3 (Slide 4/Roadmap)", "status": "PASS" if not errors else "FAIL", "errors": errors}


def generate_pdf(report, pdf_path):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("Self-Modifiable Reversible Circuits — Verification Report", styles["Title"]))
        story.append(Paragraph(f"Generated: {report['timestamp']}", styles["Normal"]))
        story.append(Spacer(1, 20))
        for v in report["verifications"]:
            story.append(Paragraph(
                f"[{v['status']}] {v['verification']}", styles["Heading2"]
            ))
            if v.get("errors"):
                for e in v["errors"]:
                    story.append(Paragraph(f"  ERROR: {e}", styles["Normal"]))
            story.append(Spacer(1, 8))
        story.append(Paragraph(f"OVERALL: {report['overall']}", styles["Heading1"]))
        doc.build(story)
        print(f"[report] PDF saved to {pdf_path}")
        return True
    except ImportError:
        print("[report] reportlab not installed; skipping PDF. Install: pip install reportlab")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 70)
    print("SELF-MODIFIABLE REVERSIBLE CIRCUITS — FULL VERIFICATION PIPELINE")
    print("=" * 70)

    # ── Step 1: Core simulation (sigma3, NAND, NOR, self-modifiable) ──────────
    print("\n[Step 1] Compiling core Verilog (sigma3, NAND, NOR, self-modifiable)...")
    compile_verilog()
    print("[Step 1] Running core simulation...")
    core_output = run_simulation()
    core_data = parse_log(core_output)

    # ── Step 2: AES simulation (XOR, field ops, obfuscation circuits) ─────────
    print("\n[Step 2] Compiling AES Verilog (XOR, GF(2^8), obfuscation)...")
    compile_aes_verilog()
    print("[Step 2] Running AES simulation...")
    aes_output = run_aes_simulation()
    aes_data = parse_log(aes_output)

    print(f"\n  Core:  sigma3={len(core_data['sigma3'])}, nand={len(core_data['nand'])}, "
          f"nor={len(core_data['nor'])}, selfmod={len(core_data['selfmod'])}")
    print(f"  AES:   xor={len(aes_data['xor'])}, fadd={len(aes_data['fadd'])}, "
          f"fmul={len(aes_data['fmul'])}, oxor={len(aes_data['oxor'])}, cobf={len(aes_data['cobf'])}")

    # ── Step 3: Run all verifications ─────────────────────────────────────────
    print("\n[Step 3] Running verifications against research paper claims...")

    verifications = [
        # Paper Slide 5 — σ3 gate truth table
        verify_truth_table(core_data["sigma3"]),
        # Paper Slide 5 — σ3 reversibility (bijection)
        verify_reversibility(core_data["sigma3"]),
        # Paper Slide 4/Roadmap — σ3 universality: NAND
        verify_nand(core_data["nand"]),
        # Paper Slide 4/Roadmap — σ3 universality: NOR
        verify_nor(core_data["nor"]),
        # Paper Slide 6 — Self-modifiable circuit
        verify_self_modifiable(core_data["selfmod"]),
        # Paper Slide 10 — XOR circuit: A⊕B = (A∨B)∧¬(A∧B)
        verify_xor_circuit(aes_data["xor"]),
        # Paper Slide 9 — Lookup table memory complexity
        verify_lookup_table_complexity(),
        # Paper Slide 11 — GF(2^8) field addition = XOR
        verify_aes_field_add(aes_data["fadd"]),
        # Paper Slide 8 & 12 — GF(2^8) field multiplication + paper example
        verify_aes_field_mul(aes_data["fmul"]),
        # Paper Slide 14 — Random XOR / moving computation
        verify_random_xor(aes_data["oxor"]),
        # Paper Slide 13 — Circuit obfuscation (polynomial routing)
        verify_circuit_obfuscation(aes_data["cobf"]),
        # Paper Slide 16 — AES S-Box obfuscation: 490 σ₃ gates
        verify_sbox_complexity(),
        # Paper Slides 2/18 — No one-way functions required
        verify_non_one_way_function_claim(),
        # Paper Slides 7/15 — Side-channel resistance
        verify_side_channel_resistance(),
        # Paper Pages 10 & 25 — General alternating location method
        verify_general_method(),
        # Paper Page 26 — XOR gate requires exactly 4 sigma3 gates
        verify_xor_gate_cost(),
        # Paper Page 26 — Permutation complexity: at most n-1 swaps, AES n=48
        verify_permutation_complexity(),
        # Paper Pages 11 & 25 — Kerckhoffs' principle violation
        verify_kerckhoffs_principle(),
        # Paper Page 4 — Quantum computing applicability (sigma3 = Fredkin gate)
        verify_quantum_applicability(),
        # Paper Page 3 — Physics obfuscation via Heisenberg uncertainty
        verify_heisenberg_obfuscation(),
        # Paper Page 4 — Long-term circuit repair potential
        verify_circuit_repair_potential(),
    ]

    overall = "PASS" if all(v["status"] == "PASS" for v in verifications) else "FAIL"

    report = {
        "title": "Self-Modifiable Reversible Circuits — Verification Report",
        "paper": "Michael Stephen Fiske, HICSS-59, Aemea Institute",
        "timestamp": datetime.datetime.now().isoformat(),
        "overall": overall,
        "total_checks": len(verifications),
        "passed": sum(1 for v in verifications if v["status"] == "PASS"),
        "failed": sum(1 for v in verifications if v["status"] == "FAIL"),
        "verifications": verifications,
    }

    # ── Step 4: Save JSON report ───────────────────────────────────────────────
    json_path = os.path.join(OUTPUT_DIR, "verification_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[report] JSON saved to {json_path}")

    # ── Step 5: Optional PDF ───────────────────────────────────────────────────
    generate_pdf(report, os.path.join(OUTPUT_DIR, "verification_report.pdf"))

    # ── Step 6: Console summary ────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    for v in verifications:
        icon = "✓" if v["status"] == "PASS" else "✗"
        print(f"  {icon} [{v['status']}] {v['verification']}")
        for e in v.get("errors", []):
            print(f"         ↳ {e}")
    print("=" * 70)
    print(f"  RESULT : {overall}  ({report['passed']}/{report['total_checks']} passed)")
    print("=" * 70)

    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()

