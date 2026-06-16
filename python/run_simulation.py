"""
run_simulation.py
Compiles and runs the Verilog simulation using Icarus Verilog.
"""

import subprocess
import os
import sys

# Ensure Homebrew binaries (iverilog, vvp) are on PATH on macOS
os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERILOG_DIR = os.path.join(BASE_DIR, "verilog")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SIM_BINARY = os.path.join(OUTPUT_DIR, "sim")
SIM_LOG = os.path.join(OUTPUT_DIR, "simulation.log")

AES_SIM_BINARY = os.path.join(OUTPUT_DIR, "sim_aes")
AES_SIM_LOG = os.path.join(OUTPUT_DIR, "simulation_aes.log")

# Core sigma3 + self-modifiable testbench
VERILOG_FILES = [
    "sigma3_reversible.v",
    "nand_from_sigma.v",
    "nor_from_sigma.v",
    "self_modifiable.v",
    "testbench.v",
]

# AES-related modules + testbench (depends on sigma3 & nand/nor)
AES_VERILOG_FILES = [
    "sigma3_reversible.v",
    "nand_from_sigma.v",
    "nor_from_sigma.v",
    "xor_from_sigma.v",
    "aes_field_add.v",
    "aes_field_mul.v",
    "obfuscated_xor.v",
    "circuit_obfuscation.v",
    "testbench_aes.v",
]


def _compile(sources, binary, label):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = ["iverilog", "-o", binary] + sources
    print(f"[compile:{label}] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[compile:{label}] ERROR:\n", result.stderr)
        sys.exit(1)
    print(f"[compile:{label}] SUCCESS")


def _run(binary, log_path, label):
    cmd = ["vvp", binary]
    print(f"[simulate:{label}] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[simulate:{label}] ERROR:\n", result.stderr)
        sys.exit(1)
    with open(log_path, "w") as f:
        f.write(result.stdout)
    print(f"[simulate:{label}] Log saved to {log_path}")
    return result.stdout


def compile_verilog():
    _compile([os.path.join(VERILOG_DIR, f) for f in VERILOG_FILES], SIM_BINARY, "core")


def compile_aes_verilog():
    _compile([os.path.join(VERILOG_DIR, f) for f in AES_VERILOG_FILES], AES_SIM_BINARY, "aes")


def run_simulation():
    return _run(SIM_BINARY, SIM_LOG, "core")


def run_aes_simulation():
    return _run(AES_SIM_BINARY, AES_SIM_LOG, "aes")


if __name__ == "__main__":
    compile_verilog()
    output = run_simulation()
    print("\n--- Core Simulation Output ---")
    print(output)

    compile_aes_verilog()
    aes_output = run_aes_simulation()
    print("\n--- AES Simulation Output ---")
    print(aes_output)
