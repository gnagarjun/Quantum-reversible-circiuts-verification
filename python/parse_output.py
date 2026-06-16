"""
parse_output.py
Parses simulation.log into structured Python data.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_LOG = os.path.join(BASE_DIR, "output", "simulation.log")


def parse_log(log_text=None):
    if log_text is None:
        with open(SIM_LOG) as f:
            log_text = f.read()

    sigma3_results = []
    nand_results = []
    nor_results = []
    selfmod_results = []
    xor_results = []
    fadd_results = []
    fmul_results = []
    oxor_results = []
    cobf_results = []

    for line in log_text.splitlines():
        line = line.strip()

        # SIGMA3 I1=0 I2=1 S=0 O1=1 O2=0 S_out=0
        m = re.match(
            r"SIGMA3 I1=(\d) I2=(\d) S=(\d) O1=(\d) O2=(\d) S_out=(\d)", line
        )
        if m:
            sigma3_results.append({
                "I1": int(m.group(1)), "I2": int(m.group(2)),
                "S": int(m.group(3)), "O1": int(m.group(4)),
                "O2": int(m.group(5)), "S_out": int(m.group(6)),
            })
            continue

        # NAND A=0 B=0 NAND_OUT=1
        m = re.match(r"NAND A=(\d) B=(\d) NAND_OUT=(\d)", line)
        if m:
            nand_results.append({
                "A": int(m.group(1)), "B": int(m.group(2)),
                "NAND_OUT": int(m.group(3)),
            })
            continue

        # NOR A=0 B=0 NOR_OUT=1
        m = re.match(r"NOR A=(\d) B=(\d) NOR_OUT=(\d)", line)
        if m:
            nor_results.append({
                "A": int(m.group(1)), "B": int(m.group(2)),
                "NOR_OUT": int(m.group(3)),
            })
            continue

        # SELFMOD S=0 I1=0 I2=0 O2=1 O4=1
        m = re.match(r"SELFMOD S=(\d) I1=(\d) I2=(\d) O2=(\d) O4=(\d)", line)
        if m:
            selfmod_results.append({
                "S": int(m.group(1)), "I1": int(m.group(2)),
                "I2": int(m.group(3)), "O2": int(m.group(4)),
                "O4": int(m.group(5)),
            })
            continue

        # XOR A=0 B=1 XOR_OUT=1
        m = re.match(r"XOR A=(\d) B=(\d) XOR_OUT=(\d)", line)
        if m:
            xor_results.append({
                "A": int(m.group(1)), "B": int(m.group(2)),
                "XOR_OUT": int(m.group(3)),
            })
            continue

        # FADD r=52 w=05 sum=57   (hex)
        m = re.match(r"FADD r=([0-9a-fA-F]+) w=([0-9a-fA-F]+) sum=([0-9a-fA-F]+)", line)
        if m:
            fadd_results.append({
                "r": int(m.group(1), 16), "w": int(m.group(2), 16),
                "sum": int(m.group(3), 16),
            })
            continue

        # FMUL a=52 b=05 product=01  (hex)
        m = re.match(r"FMUL a=([0-9a-fA-F]+) b=([0-9a-fA-F]+) product=([0-9a-fA-F]+)", line)
        if m:
            fmul_results.append({
                "a": int(m.group(1), 16), "b": int(m.group(2), 16),
                "product": int(m.group(3), 16),
            })
            continue

        # OXOR x=0 y=1 b=0 z=0 w=1
        m = re.match(r"OXOR x=(\d) y=(\d) b=(\d) z=(\d) w=(\d)", line)
        if m:
            oxor_results.append({
                "x": int(m.group(1)), "y": int(m.group(2)),
                "b": int(m.group(3)), "z": int(m.group(4)),
                "w": int(m.group(5)),
            })
            continue

        # COBF p1=0 p4=1 p5=0 b=1 u=1 v=1 w=0 z=0
        m = re.match(
            r"COBF p1=(\d) p4=(\d) p5=(\d) b=(\d) u=(\d) v=(\d) w=(\d) z=(\d)", line
        )
        if m:
            cobf_results.append({
                "p1": int(m.group(1)), "p4": int(m.group(2)),
                "p5": int(m.group(3)), "b":  int(m.group(4)),
                "u":  int(m.group(5)), "v":  int(m.group(6)),
                "w":  int(m.group(7)), "z":  int(m.group(8)),
            })

    return {
        "sigma3": sigma3_results,
        "nand": nand_results,
        "nor": nor_results,
        "selfmod": selfmod_results,
        "xor": xor_results,
        "fadd": fadd_results,
        "fmul": fmul_results,
        "oxor": oxor_results,
        "cobf": cobf_results,
    }


if __name__ == "__main__":
    import json
    data = parse_log()
    print(json.dumps(data, indent=2))

