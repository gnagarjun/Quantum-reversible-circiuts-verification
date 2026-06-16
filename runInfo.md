# runInfo.md — How to Run the Verification Suite

**Project:** Self-Modifiable Reversible Circuits — Verification Framework  
**Paper:** Michael Stephen Fiske, HICSS-59, Aemea Institute, January 9, 2026

---

## Project Structure

```
Quantum-reversible-circiuts-verification/
├── ResearchPaper.md            # Source-of-truth paper (slides)
├── runInfo.md                  # This file
├── Readme.md                   # Project overview
│
├── verilog/                    # Synthesisable Verilog gate implementations
│   ├── sigma3_reversible.v     # σ₃ gate (core reversible primitive)
│   ├── nand_from_sigma.v       # NAND built from σ₃
│   ├── nor_from_sigma.v        # NOR built from σ₃
│   ├── xor_from_sigma.v        # XOR built from σ₃-based NANDs
│   ├── aes_field_add.v         # GF(2⁸) addition (8-bit XOR)
│   ├── aes_field_mul.v         # GF(2⁸) multiplication (xtime + accumulate)
│   ├── self_modifiable.v       # Self-modifiable NAND↔NOR circuit
│   ├── obfuscated_xor.v        # Random XOR circuit (Slide 14)
│   ├── circuit_obfuscation.v   # Polynomial routing circuit (Slide 13)
│   ├── testbench.v             # Testbench: σ₃, NAND, NOR, self-modifiable
│   └── testbench_aes.v         # Testbench: XOR, field ops, obfuscation
│
├── python/                     # Verification scripts
│   ├── run_simulation.py       # Compile + run Verilog simulations
│   ├── parse_output.py         # Parse simulation logs into Python dicts
│   ├── verify_truth_table.py   # Verify σ₃ truth table (Slide 5)
│   ├── verify_reversibility.py # Verify σ₃ bijection (Slide 5)
│   ├── verify_self_modifiable.py # Verify S-controlled NAND↔NOR (Slide 6)
│   ├── verify_xor_circuit.py   # Verify XOR formula (Slide 10)
│   ├── verify_aes_field_ops.py # Verify GF(2⁸) add/mul + lookup table (Slides 8,9,11,12)
│   ├── verify_obfuscation.py   # Verify random XOR + polynomial routing (Slides 13,14)
│   ├── verify_sbox_complexity.py # Verify 490 gate count + security claims (Slides 16,17,2,18)
│   └── generate_report.py      # MAIN ENTRY POINT — runs everything
│
├── output/                     # Generated at runtime
│   ├── sim                     # Compiled core simulation binary
│   ├── sim_aes                 # Compiled AES simulation binary
│   ├── simulation.log          # Core simulation output
│   ├── simulation_aes.log      # AES simulation output
│   └── verification_report.json  # Full JSON verification report
│
└── docs/
    └── research_notes.md       # Detailed notes on all concepts + verification mapping
```

---

## Prerequisites

### 1. Install Icarus Verilog (iverilog)

**macOS (Homebrew):**
```bash
brew install icarus-verilog
```

**Ubuntu/Debian:**
```bash
sudo apt-get install iverilog
```

**Verify installation:**
```bash
iverilog -V
vvp -V
```

### 2. Python 3 (no extra packages required)
The core pipeline uses only Python standard library.

**Optional — PDF report generation:**
```bash
pip install reportlab
```

---

## Running the Full Verification Suite

### One-command run (recommended):
```bash
cd /path/to/Quantum-reversible-circiuts-verification
python3 python/generate_report.py
```

This single command:
1. Compiles all core Verilog (σ₃, NAND, NOR, self-modifiable)
2. Runs the core simulation
3. Compiles all AES Verilog (XOR, GF(2⁸), obfuscation circuits)
4. Runs the AES simulation
5. Parses both simulation logs
6. Runs all 15 verifications against the paper's claims
7. Saves `output/verification_report.json`
8. Prints a pass/fail summary to the console

**Expected output:**
```
======================================================================
SELF-MODIFIABLE REVERSIBLE CIRCUITS — FULL VERIFICATION PIPELINE
======================================================================

[Step 1] Compiling core Verilog...
[compile:core] SUCCESS
[Step 1] Running core simulation...
[simulate:core] Log saved to output/simulation.log

[Step 2] Compiling AES Verilog...
[compile:aes] SUCCESS
[Step 2] Running AES simulation...
[simulate:aes] Log saved to output/simulation_aes.log

  Core:  sigma3=8, nand=4, nor=4, selfmod=8
  AES:   xor=4, fadd=3, fmul=5, oxor=8, cobf=16

[Step 3] Running verifications...
...
======================================================================
VERIFICATION SUMMARY
======================================================================
  ✓ [PASS] Truth Table
  ✓ [PASS] Reversibility
  ✓ [PASS] NAND from σ3 (Slide 4/Roadmap)
  ✓ [PASS] NOR from σ3 (Slide 4/Roadmap)
  ✓ [PASS] Self-Modifiable Circuit
  ✓ [PASS] XOR Circuit from sigma3 (Slide 10)
  ✓ [PASS] Lookup Table Memory Complexity — Slide 9
  ✓ [PASS] AES GF(2^8) Field Addition — Slide 11
  ✓ [PASS] AES GF(2^8) Field Multiplication — Slides 8 & 12
  ✓ [PASS] Random XOR Circuit (Moving Computation) — Slide 14
  ✓ [PASS] Circuit Obfuscation (Polynomial Routing) — Slide 13
  ✓ [PASS] AES S-Box Obfuscation Gate Complexity — Slide 16
  ✓ [PASS] No One-Way Functions Required — Slides 2 & 18
  ✓ [PASS] Side-Channel Resistance via Moving Computation — Slides 7 & 15
  ✓ [PASS] General Alternating Location Method — Slide 17
======================================================================
  RESULT : PASS  (15/15 passed)
======================================================================
```

---

## Running Individual Steps

### Step A — Compile and simulate only (no Python verification)

**Core simulation (σ₃, NAND, NOR, self-modifiable):**
```bash
iverilog -o output/sim \
  verilog/sigma3_reversible.v \
  verilog/nand_from_sigma.v \
  verilog/nor_from_sigma.v \
  verilog/self_modifiable.v \
  verilog/testbench.v

vvp output/sim
```

**AES simulation (XOR, GF(2⁸) add/mul, obfuscation):**
```bash
iverilog -o output/sim_aes \
  verilog/sigma3_reversible.v \
  verilog/nand_from_sigma.v \
  verilog/nor_from_sigma.v \
  verilog/xor_from_sigma.v \
  verilog/aes_field_add.v \
  verilog/aes_field_mul.v \
  verilog/obfuscated_xor.v \
  verilog/circuit_obfuscation.v \
  verilog/testbench_aes.v

vvp output/sim_aes
```

### Step B — Run only the simulation driver (compile + run, no verification)
```bash
python3 python/run_simulation.py
```

### Step C — Run individual verifiers (requires simulation logs to exist)

First run `python3 python/run_simulation.py`, then:

```bash
# Parse simulation output
python3 python/parse_output.py

# Verify individual claims
python3 python/verify_truth_table.py
python3 python/verify_reversibility.py
python3 python/verify_self_modifiable.py
python3 python/verify_xor_circuit.py
python3 python/verify_aes_field_ops.py
python3 python/verify_obfuscation.py
python3 python/verify_sbox_complexity.py
```

---

## What Each Verification Checks

### Core Gate Verifications (from `testbench.v`)

| Verifier | Paper Slide | What It Checks |
|----------|-------------|----------------|
| `verify_truth_table.py` | Slide 5 | All 8 rows of σ₃ truth table match exactly |
| `verify_reversibility.py` | Slide 5 | All 8 outputs are distinct (bijection) |
| `verify_nand()` in report | Slide 4 | NAND(0,0)=1, NAND(0,1)=1, NAND(1,0)=1, NAND(1,1)=0 |
| `verify_nor()` in report | Slide 4 | NOR(0,0)=1, NOR(0,1)=0, NOR(1,0)=0, NOR(1,1)=0 |
| `verify_self_modifiable.py` | Slide 6 | S=0: O4=NAND O2=NOR; S=1: O4=NOR O2=NAND |

### AES & Obfuscation Verifications (from `testbench_aes.v`)

| Verifier | Paper Slide | What It Checks |
|----------|-------------|----------------|
| `verify_xor_circuit.py` | Slide 10 | A⊕B = (A∨B)∧¬(A∧B) for all 4 input combos |
| `verify_lookup_table_complexity()` | Slide 9 | n=32: 137,438,953,472 bits; n=64: 1,180,591,620,717,411,303,424 bits |
| `verify_aes_field_add()` | Slide 11 | 8-bit XOR + commutativity/identity/self-inverse properties |
| `verify_aes_field_mul()` | Slides 8,12 | GF(2⁸) multiply: paper example 0x52×0x05=0x01 + field axioms |
| `verify_random_xor()` | Slide 14 | b=1: z=x⊕y,w=x; b=0: z=x,w=x⊕y — all 8 combos |
| `verify_circuit_obfuscation()` | Slide 13 | b-controlled routing of p4/p5 XOR values — all 16 combos |

### Mathematical & Structural Verifications (Python-only, no Verilog)

| Verifier | Paper Slide | What It Checks |
|----------|-------------|----------------|
| `verify_sbox_complexity()` | Slide 16 | 7×7×10 = 490 σ₃ gates |
| `verify_non_one_way_function_claim()` | Slides 2,18 | Only σ₃ and XOR used — no one-way function assumptions |
| `verify_side_channel_resistance()` | Slides 7,15 | Moving computation hinders power/timing/acoustic attacks |
| `verify_general_method()` | Slide 17 | f/g alternate locations based on control bit b |

---

## Reading the Output Files

### `output/simulation.log`
Raw output from the core Verilog testbench. Lines prefixed:
- `SIGMA3 I1=.. I2=.. S=.. O1=.. O2=.. S_out=..` — σ₃ gate test row
- `NAND A=.. B=.. NAND_OUT=..` — NAND test row
- `NOR A=.. B=.. NOR_OUT=..` — NOR test row
- `SELFMOD S=.. I1=.. I2=.. O2=.. O4=..` — self-modifiable test row

### `output/simulation_aes.log`
Raw output from the AES Verilog testbench. Lines prefixed:
- `XOR A=.. B=.. XOR_OUT=..` — XOR test row
- `FADD r=.. w=.. sum=..` — field addition (hex values)
- `FMUL a=.. b=.. product=..` — GF(2⁸) multiplication (hex values)
- `OXOR x=.. y=.. b=.. z=.. w=..` — obfuscated XOR test row
- `COBF p1=.. p4=.. p5=.. b=.. u=.. v=.. w=.. z=..` — circuit obfuscation test row

### `output/verification_report.json`
Structured JSON with:
```json
{
  "title": "...",
  "paper": "...",
  "timestamp": "...",
  "overall": "PASS",
  "total_checks": 15,
  "passed": 15,
  "failed": 0,
  "verifications": [
    {
      "verification": "Truth Table",
      "status": "PASS",
      "checked": 8,
      "errors": []
    },
    ...
  ]
}
```

---

## Troubleshooting

### `iverilog: command not found`
Add Homebrew to PATH:
```bash
export PATH="/opt/homebrew/bin:$PATH"
python3 python/generate_report.py
```
Or add it permanently to `~/.zshrc`:
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### `ImportError` on Python scripts
Always run from the project root:
```bash
cd /path/to/Quantum-reversible-circiuts-verification
python3 python/generate_report.py
```

### Simulation produces 0 rows for a category
Check `output/simulation.log` or `output/simulation_aes.log` directly for the raw output. Confirm the `$display` format in the testbench matches the regex in `parse_output.py`.

### PDF not generated
Install reportlab:
```bash
pip install reportlab
python3 python/generate_report.py
```

---

## Extending the Suite

To add a new verification:
1. Add the circuit to a `.v` file in `verilog/`
2. Add test stimulus with `$display` in the appropriate testbench
3. Add a parser regex in `parse_output.py`
4. Write a `verify_*.py` file with the expected behaviour
5. Import and call it in `generate_report.py`'s `verifications` list

