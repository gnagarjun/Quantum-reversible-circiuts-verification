# Sigma3 Reversible Gate Verification Framework

## Project Goal

This project provides a verification framework for validating the claims made in the paper regarding:

1. The σ₃ reversible gate
2. Self-modifiable hardware circuits
3. Dynamic function switching (NAND ↔ NOR)
4. Reversible logic properties
5. Functional correctness under exhaustive simulation

The framework combines:

* Verilog (hardware implementation)
* Python (automation and validation)
* Icarus Verilog (simulation engine)

---

# Research Questions

## RQ1

Does the σ₃ gate behave exactly according to its published truth table?

---

## RQ2

Is the σ₃ gate reversible?

A reversible gate must satisfy:

* Every input state maps to a unique output state.
* No information is lost.
* Inputs can be reconstructed from outputs.

---

## RQ3

Can σ₃ be used to construct universal logic functions?

Specifically:

* AND
* OR
* NAND
* NOR

---

## RQ4

Can the self-modifiable circuit dynamically change functionality without modifying physical wiring?

The paper claims:

When S = 1:

O4 = NOR(I1,I2)

O2 = NAND(I1,I2)

When S = 0:

O4 = NAND(I1,I2)

O2 = NOR(I1,I2)

This project verifies that claim.

---

# What We Are Verifying

## Verification 1

σ₃ Reversible Gate Truth Table

Input:

I1
I2
S

Output:

O1
O2
S

Expected behavior:

If S = 0:

swap(I1,I2)

If S = 1:

pass-through(I1,I2)

Success Criteria:

Simulation output exactly matches the truth table in the paper.

---

## Verification 2

Reversibility

For every input:

(I1,I2,S)

Verify:

Input -> Output mapping is unique.

No two inputs may produce the same output.

Success Criteria:

Number of unique outputs equals number of unique inputs.

Expected:

8 inputs
8 outputs

Perfect bijection.

---

## Verification 3

NAND Construction

Verify:

NAND = NOT(AND)

using σ₃-based construction.

Success Criteria:

Output matches classical NAND truth table.

---

## Verification 4

NOR Construction

Verify:

NOR = NOT(OR)

using σ₃-based construction.

Success Criteria:

Output matches classical NOR truth table.

---

## Verification 5

Self-Modifiable Behavior

Verify:

Changing S changes functionality.

Without changing:

* inputs
* outputs
* wiring

Success Criteria:

Output functions swap exactly as described in the paper.

---

# Project Structure

project/

├── README.md

├── verilog/

│   ├── sigma3_reversible.v

│   ├── nand_from_sigma.v

│   ├── nor_from_sigma.v

│   ├── self_modifiable.v

│   └── testbench.v

├── python/

│   ├── run_simulation.py

│   ├── parse_output.py

│   ├── verify_truth_table.py

│   ├── verify_reversibility.py

│   ├── verify_self_modifiable.py

│   └── generate_report.py

├── output/

│   ├── simulation.log

│   ├── verification_report.json

│   └── verification_report.pdf

└── docs/

```
└── research_notes.md
```

---

# Verification Workflow

Step 1

Compile Verilog

iverilog -o sim verilog/*.v

---

Step 2

Run simulation

vvp sim > output/simulation.log

---

Step 3

Python reads simulation results

simulation.log

---

Step 4

Python compares outputs against:

* expected truth table
* reversibility requirements
* NAND truth table
* NOR truth table

---

Step 5

Generate verification report

PASS / FAIL

---

# Reversibility Validation

The most important test.

Create a Python dictionary:

Input -> Output

Example:

(0,1,0) -> (1,0,0)

Store every mapping.

If:

len(inputs) == len(unique_outputs)

then:

Gate is reversible.

Otherwise:

Gate is not reversible.

---

# Self-Modifiable Circuit Validation

For every input combination:

Run:

S=0

Store outputs.

Run:

S=1

Store outputs.

Verify:

O2 and O4 swap functions exactly as described.

---

# Deliverables

At project completion the framework should produce:

1. Simulation logs
2. Truth-table verification
3. Reversibility proof
4. Self-modification proof
5. PDF report
6. Waveform screenshots

---

# Success Criteria

The proof-of-concept is considered successful when:

✓ σ₃ truth table matches

✓ Reversibility confirmed

✓ NAND construction verified

✓ NOR construction verified

✓ Self-modifiable behavior verified

✓ Simulation results reproducible

✓ Automated verification passes

---

# Future Extensions

Phase 2

* GTKWave visualization
* Formal verification

Phase 3

* FPGA implementation

Phase 4

* Quantum gate mapping

Phase 5

* Benchmark against Toffoli and Fredkin gates

Phase 6

* Research publication package
