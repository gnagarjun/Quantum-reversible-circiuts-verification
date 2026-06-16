# Research Notes: Self-Modifiable Reversible Circuits
**Paper:** Michael Stephen Fiske, HICSS-59, Aemea Institute, January 9, 2026

---

## Table of Contents
1. [Background: Why Reversible Computing?](#1-background-why-reversible-computing)
2. [The σ₃ Gate](#2-the-σ₃-gate)
3. [σ₃ is Universal: NAND and NOR](#3-σ₃-is-universal-nand-and-nor)
4. [XOR from NAND](#4-xor-from-nand)
5. [Self-Modifiable Circuits](#5-self-modifiable-circuits)
6. [AES S-Box Background: GF(2⁸) Arithmetic](#6-aes-s-box-background-gf28-arithmetic)
7. [Circuit Addition and Multiplication](#7-circuit-addition-and-multiplication)
8. [Circuit Obfuscation via σ₃](#8-circuit-obfuscation-via-σ₃)
9. [Random XOR / Moving Computation](#9-random-xor--moving-computation)
10. [AES S-Box Obfuscation Complexity](#10-aes-s-box-obfuscation-complexity)
11. [Security Claims](#11-security-claims)
12. [How We Verify Each Claim in Code](#12-how-we-verify-each-claim-in-code)

---

## 1. Background: Why Reversible Computing?

### Landauer's Principle (1961)
A logic gate is **reversible** if its function is one-to-one (bijective):
- x₁ ≠ x₂ → f(x₁) ≠ f(x₂)

Classical gates like AND, OR, NAND, NOR are **not reversible**:
- OR(1,0) = OR(0,1) = 1 — two inputs produce the same output, so you cannot recover the input from the output.

**Consequence:** Non-invertible operations executed in physical hardware must **increase entropy** and produce **heat**. Every bit of information erased generates kT·ln(2) joules of heat.

### Bennett (1973)
Proved it is theoretically possible to build **logically reversible** computing machines — every computation can be made reversible by adding ancilla (helper) bits.

### Why This Paper Matters
The paper extends reversible computing to **self-modifiable** circuits:
- Circuits can change the Boolean function they compute without physically altering connections.
- This is implemented entirely using reversible σ₃ gates.
- No reliance on one-way functions (unlike Yao 1982 or Barak 2010).

---

## 2. The σ₃ Gate

### Definition (Paper Slide 5)
A 3-input, 3-output reversible gate:

| I1 | I2 | S | O1 | O2 | S_out |
|----|----|----|----|----|-------|
|  0 |  0 | 0 |  0 |  0 |   0   |
|  0 |  1 | 0 |  1 |  0 |   0   |
|  1 |  0 | 0 |  0 |  1 |   0   |
|  1 |  1 | 0 |  1 |  1 |   0   |
|  0 |  0 | 1 |  0 |  0 |   1   |
|  0 |  1 | 1 |  0 |  1 |   1   |
|  1 |  0 | 1 |  1 |  0 |   1   |
|  1 |  1 | 1 |  1 |  1 |   1   |

**Rule:**
- **S = 0** → **swap**: O1 = I2, O2 = I1, S_out = 0
- **S = 1** → **pass-through**: O1 = I1, O2 = I2, S_out = 1

### Reversibility
With 3 binary inputs there are 2³ = 8 possible states. For σ₃ to be reversible, all 8 input states must map to **8 distinct output states** (bijection). This is verified exhaustively by our simulation.

### Verilog Implementation (`sigma3_reversible.v`)
```verilog
assign O1    = S ? I1 : I2;   // pass-through if S=1, swap if S=0
assign O2    = S ? I2 : I1;
assign S_out = S;
```
S is always preserved in the output — this is what makes the gate reversible (the control signal is never destroyed).

---

## 3. σ₃ is Universal: NAND and NOR

### NAND from σ₃ (Paper Slide 4 Roadmap)

**Key insight:** Set the control pin S = A (first input becomes its own control):

```
σ₃(A, B, S=A):
  A=0 (swap)  → O1=B, O2=A=0   → O2 = 0 = A AND B  ✓ (since A=0)
  A=1 (pass)  → O1=A=1, O2=B   → O2 = B = A AND B  ✓ (since A=1)
```

Therefore **O2 = AND(A,B)**, and **NAND = NOT(O2) = ~O2**.

Verilog (`nand_from_sigma.v`):
```verilog
sigma3_reversible g1(.I1(A), .I2(B), .S(A), .O1(O1), .O2(O2), .S_out(S_out));
assign NAND_OUT = ~O2;
```

### NOR from σ₃

**Key insight:** NOR(A,B) = NOT(A) AND NOT(B). Apply σ₃ with inverted inputs and S = ~A:

```
σ₃(~A, ~B, S=~A):
  ~A=1 (pass) → O2 = ~B             → only when A=0: O2 = ~B. But A=0,B=0→O2=1=NOR ✓
  ~A=0 (swap) → O2 = ~A = 0         → when A=1: O2=0=NOR(1,anything) ✓
```

More precisely, O2 = AND(~A, ~B) = NOR(A,B).

Verilog (`nor_from_sigma.v`):
```verilog
assign nA = ~A;
assign nB = ~B;
sigma3_reversible g1(.I1(nA), .I2(nB), .S(nA), .O1(O1), .O2(O2), .S_out(S_out));
assign NOR_OUT = O2;
```

---

## 4. XOR from NAND

### Formula (Paper Slide 10)
```
A ⊕ B = (A ∨ B) ∧ ¬(A ∧ B)
```

### 4-NAND XOR Construction
The classic way to build XOR from only NAND gates:
```
N  = NAND(A, B)
AN = NAND(A, N)
BN = NAND(B, N)
XOR = NAND(AN, BN)
```
All four NAND gates are built from σ₃, making this a **pure σ₃ implementation of XOR**.

Verilog (`xor_from_sigma.v`):
```verilog
nand_from_sigma g1(.A(A),  .B(B),  .NAND_OUT(N));
nand_from_sigma g2(.A(A),  .B(N),  .NAND_OUT(AN));
nand_from_sigma g3(.A(B),  .B(N),  .NAND_OUT(BN));
nand_from_sigma g4(.A(AN), .B(BN), .NAND_OUT(XOR_OUT));
```

---

## 5. Self-Modifiable Circuits

### Concept (Paper Slide 6)
A self-modifiable circuit changes the Boolean function it computes **without changing physical connections**. The σ₃ gate's control pin S routes outputs differently, effectively swapping which output wire gets which computed result.

### Implementation (`self_modifiable.v`)
The circuit computes both NAND(I1,I2) and NOR(I1,I2) simultaneously, then uses a final σ₃ gate to route results:

```
σ₃(nor_result, nand_result, S):
  S=0 (swap): O4=nand_result, O2=nor_result   → O4=NAND, O2=NOR
  S=1 (pass): O4=nor_result,  O2=nand_result  → O4=NOR,  O2=NAND
```

**Behavior:**
- **S = 0**: O4 = NAND(I1,I2), O2 = NOR(I1,I2)
- **S = 1**: O4 = NOR(I1,I2),  O2 = NAND(I1,I2)

Changing S swaps the functionality of output wires O2 and O4 — **the circuit is self-modifiable**.

---

## 6. AES S-Box Background: GF(2⁸) Arithmetic

### Field Definition (Paper Slide 8)
The AES S-Box operates over the **Galois Field GF(2⁸)**:

- **Base field:** F₂ = {0, 1}, addition = XOR, multiplication = AND
- **Polynomial ring:** F₂[x] (polynomials with binary coefficients)
- **AES irreducible polynomial:** m(x) = x⁸ + x⁴ + x³ + x + 1 (hex: 0x11B)
- **Field:** F₂[x] / m(x)  — polynomials mod m(x)

Each 8-bit byte represents a degree-7 polynomial:
```
byte 0x52 = 01010010₂ = x⁶ + x⁴ + x¹
byte 0x05 = 00000101₂ = x² + 1
```

### Paper Example (Slide 8)
```
p(x) = x⁶ + x⁴ + x = 0x52
q(x) = x² + 1 = 0x05
p(x) × q(x) mod m(x) = 1
```

This means 0x52 and 0x05 are **multiplicative inverses** in GF(2⁸). Verified by simulation.

**Derivation:**
```
p×q = (x⁶+x⁴+x)(x²+1) = x⁸+x⁶ + x⁶+x⁴ + x³+x
    = x⁸ + x⁴ + x³ + x                (x⁶ terms cancel in F₂)
    ≡ (x⁴+x³+x+1) + x⁴+x³+x = 1     (since x⁸ ≡ x⁴+x³+x+1 mod m(x))
```

### Why Not a Lookup Table? (Paper Slide 9)
An n-input lookup table needs **n × 2ⁿ bits** of memory:
- n = 32: 32 × 2³² = **137,438,953,472 bits** ≈ 17 GB
- n = 64: 64 × 2⁶⁴ = **1,180,591,620,717,411,303,424 bits** — physically impossible

This motivates building AES S-Box from arithmetic circuits (NAND/NOR/XOR from σ₃).

---

## 7. Circuit Addition and Multiplication

### Circuit Addition (Paper Slide 11)
GF(2⁸) addition = bitwise XOR of the 8 polynomial coefficient bits:
```
add_polynomials(r, w) = [r₁⊕w₁, r₂⊕w₂, ..., r₈⊕w₈]
```

**Algebraic properties verified:**
- Commutativity: a + b = b + a
- Identity: a + 0 = a
- Self-inverse: a + a = 0

Verilog (`aes_field_add.v`): 8 parallel `xor_from_sigma` instances, one per bit.

### Circuit Multiplication (Paper Slide 12)
GF(2⁸) multiplication uses the **xtime** (multiply-by-x) operation:
```
xtime(a):
  if a[7] == 0: return a << 1
  else:         return (a << 1) XOR 0x1B
```

Full multiplication (Russian-peasant algorithm):
```
gf_mul(a, b) = XOR of xtime^i(a) for each bit i where b[i] == 1
```

**Algebraic properties verified:**
- Multiplicative identity: a × 1 = a
- Zero: a × 0 = 0
- Commutativity: a × b = b × a
- Distributivity: a×(b+c) = a×b + a×c

Verilog (`aes_field_mul.v`): chain of 8 `xtime` modules + conditional XOR accumulation.

---

## 8. Circuit Obfuscation via σ₃

### The Core Idea (Paper Slide 13)
Given polynomial coefficients p1, p4, p5, compute XOR combinations and route them through σ₃:

**b = 1 (pass-through):**
```
u = p4,       v = p4 ⊕ p1,   w = p5,       z = p5 ⊕ p1
```

**b = 0 (swap):**
```
u = p5 ⊕ p1,  v = p5,        w = p4 ⊕ p1,  z = p4
```

**Implementation uses exactly 2 σ₃ gates:**
```
Gate 1: σ₃(p4, xor_p5_p1, b)    → outputs (u, z)
Gate 2: σ₃(xor_p4_p1, p5, b)    → outputs (v, w)
```

Verification:
- b=1: G1 passes → u=p4, z=p5⊕p1 ✓;  G2 passes → v=p4⊕p1, w=p5 ✓
- b=0: G1 swaps  → u=p5⊕p1, z=p4 ✓;  G2 swaps  → v=p5, w=p4⊕p1 ✓

The XOR results physically **move between wire locations** based on b — without changing any wiring. An observer watching power on wire `u` sees p4 when b=1 and p5⊕p1 when b=0.

---

## 9. Random XOR / Moving Computation

### Random XOR Circuit (Paper Slide 14)
The simplest example of "moving computation":

**b = 1:**  z = x ⊕ y,  w = x
**b = 0:**  z = x,      w = x ⊕ y

**Implementation:**
```
xor_xy = XOR(x, y)          // built from NAND from σ₃
σ₃(xor_xy, x, b):
  b=1 (pass): O1=xor_xy→z, O2=x→w      z=x⊕y ✓
  b=0 (swap): O1=x→z,      O2=xor_xy→w  z=x   ✓
```

The XOR result is always **computed** but its **physical location** (which output wire it appears on) changes with b. If b is chosen randomly each invocation, a power-analysis attacker cannot consistently locate the XOR computation.

### General Method (Paper Slide 17)
For any two functions f and g:
- b=1: location A gets f-result, location B gets g-result
- b=0: location A gets g-result, location B gets f-result

This is implemented with a single σ₃ gate feeding results to two output wires.

---

## 10. AES S-Box Obfuscation Complexity

### Gate Count (Paper Slide 16)
The AES S-Box multiplication circuit has:
- **7 layers** of polynomial multiplication
- **7 swaps** per layer (one per coefficient that needs obfuscating)
- **10 σ₃ gates** per swap (to route the multi-bit values)

**Total: 7 × 7 × 10 = 490 σ₃ gates**

This provides a concrete, measurable cost for obfuscating the entire AES S-Box computation such that the physical location of each multiplication result moves unpredictably per execution.

---

## 11. Security Claims

### No One-Way Functions (Slides 2 & 18)
Unlike Yao (1982) secure multi-party computation or Barak et al. (2010) obfuscation:
- Our method uses **only σ₃ gates** (provably reversible) and **XOR** (also reversible)
- No hash functions, RSA, elliptic curves, or discrete logarithms
- Security relies on **physical space-time uncertainty** (Heisenberg uncertainty principle)
- There is no mathematical proof that one-way functions exist — this approach avoids that assumption entirely

### Side-Channel Attack Resistance (Slides 7 & 15)
Moving computation hinders:
| Attack | How σ₃ routing helps |
|--------|----------------------|
| **Power analysis** | XOR result appears on different wire each run → inconsistent power trace |
| **Timing attacks** | Computation location changes → no fixed timing signature |
| **Acoustic attacks** | Different physical gates activated per run → different acoustic profile |
| **Execution bypass** | Attacker cannot reliably locate the targeted computation |

### Violates Kerckhoffs's Principle Assumptions (Slide 7)
Kerckhoffs assumes the algorithm is known but the key is secret. Here, **even knowing the circuit design**, an adversary cannot predict *where* a given computation physically executes — the location is determined by a random control bit b that changes each invocation.

---

## 12. How We Verify Each Claim in Code

| Paper Slide | Claim | Verilog Module | Python Verifier |
|-------------|-------|---------------|-----------------|
| Slide 5 | σ₃ truth table (8 rows) | `sigma3_reversible.v` + `testbench.v` | `verify_truth_table.py` |
| Slide 5 | σ₃ is reversible (bijection) | `sigma3_reversible.v` + `testbench.v` | `verify_reversibility.py` |
| Slide 4 | σ₃ implements NAND | `nand_from_sigma.v` + `testbench.v` | `generate_report.py::verify_nand()` |
| Slide 4 | σ₃ implements NOR | `nor_from_sigma.v` + `testbench.v` | `generate_report.py::verify_nor()` |
| Slide 6 | Self-modifiable: S swaps NAND↔NOR | `self_modifiable.v` + `testbench.v` | `verify_self_modifiable.py` |
| Slide 10 | XOR = (A∨B)∧¬(A∧B) | `xor_from_sigma.v` + `testbench_aes.v` | `verify_xor_circuit.py` |
| Slide 9 | Lookup table memory: n×2ⁿ bits | *(math only)* | `verify_aes_field_ops.py::verify_lookup_table_complexity()` |
| Slide 11 | Field addition = bitwise XOR | `aes_field_add.v` + `testbench_aes.v` | `verify_aes_field_ops.py::verify_aes_field_add()` |
| Slides 8,12 | GF(2⁸) multiply; 0x52×0x05=1 | `aes_field_mul.v` + `testbench_aes.v` | `verify_aes_field_ops.py::verify_aes_field_mul()` |
| Slide 14 | Random XOR: b routes XOR result | `obfuscated_xor.v` + `testbench_aes.v` | `verify_obfuscation.py::verify_random_xor()` |
| Slide 13 | Circuit obfuscation: polynomial routing | `circuit_obfuscation.v` + `testbench_aes.v` | `verify_obfuscation.py::verify_circuit_obfuscation()` |
| Slide 16 | 7×7×10 = 490 σ₃ gates | *(math only)* | `verify_sbox_complexity.py::verify_sbox_complexity()` |
| Slides 2,18 | No one-way functions needed | *(structural analysis)* | `verify_sbox_complexity.py::verify_non_one_way_function_claim()` |
| Slides 7,15 | Side-channel resistance | *(structural analysis)* | `verify_sbox_complexity.py::verify_side_channel_resistance()` |
| Slide 17 | General alternating location method | *(structural analysis)* | `verify_sbox_complexity.py::verify_general_method()` |

### Verification Methodology

**Hardware-level (Verilog + Icarus Verilog):**
Every Boolean circuit claim is implemented in synthesisable Verilog, compiled with `iverilog`, simulated with `vvp`, and the output is parsed and checked against expected truth tables.

**Mathematical-level (Python):**
Field arithmetic properties (commutativity, distributivity, identity) and complexity calculations are verified in pure Python as a cross-check.

**Structural-level (Python):**
Architectural claims (no one-way functions, side-channel resistance) are verified by code inspection — confirming only σ₃ gates and XOR operations are used in the obfuscation pipeline.
