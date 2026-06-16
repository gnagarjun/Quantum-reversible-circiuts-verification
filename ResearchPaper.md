# Self-Modifiable Reversible Circuits

Michael Stephen Fiske  
HICSS-59  
Aemea Institute  
January 9, 2026

---

# Introduction Reversible Circuits Motivation AES S-Box Circuits Moving Computation Summary

# Self-Modifiable Reversible Circuits

---

# 1. Discovery of Reversible Computing

## Landauer (1961)

- Computers are implemented with devices (gates) that are not 1-to-1.
- A function f is 1-to-1 if:
    - x1 ≠ x2 implies f(x1) ≠ f(x2)
- AND, OR, NAND, NOR are not 1-to-1.
    - OR(1,0) = OR(0,1)
- Non-invertible math operations executed in physical devices must increase entropy and produce heat.

---

## Bennett (1973)

- It is theoretically possible to build logically reversible computing machines.
- Fundamental relationship exists between:
    - Physics
    - Information
    - Computation

---

# 2. Contributions of Self-Modifiable Reversible Circuits

- Extends Reversible Computing:
    - Circuits change the Boolean function they compute without physically altering connections or components.
- Enables unpredictable execution of machine instructions on different gates and at different physical locations on the circuit.
- Physics obfuscation based on Space-Time and Heisenberg uncertainty principle.
- Cryptography based on complexity theory relies on algebraic structure of the algorithm.

> Our methods do not rely upon the existence of one-way functions.

---

## Contributions II

- Enables Hindering Cryptanalysis Attacks.
- Unpredictably moves the AES S-Box computation.
- Likely to be applicable to quantum computing.
- Long-term potential for repairing circuits.

---

# 3. Related Work

- “Conservative Logic” (Fredkin & Toffoli, 1982)
- Yao (1982): secure multi-party computation (depends on one-way functions)
- Barak et al. (2010): impossible to obfuscate a program (depends on one-way functions)
- There is no math proof that one-way functions exist.

---

# 4. Roadmap

- Reversible gate σ3
- Show σ3 is universal (NAND, NOR)
- Self-modifiable circuits
- AES S-box circuits
- Obfuscation of S-box circuits
- Moving computation across circuit space

---

# 5. Reversible σ3 Gate

If S = 0 → swap I1 and I2  
If S = 1 → no swap

Inputs:
- Ain, Bin, S

Outputs:
- Aout, Bout

---

## 3-bit Reversible Gate Logic

| I1 | I2 | S | O1 | O2 | S |
|----|----|---|----|----|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 1 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 |

---

# σ3 is Universal

- Can implement NAND
- Can implement NOR

---

# 6. Self-Modifiable Circuit

A self-modifiable circuit:

- Function at a gate output can change
- Without changing physical connections

Mechanism:

- Routing outputs to different physical locations
- Using randomness
- Computation moves unpredictably across circuit

---

# 7. Motivation for Unpredictable Circuits

- Each AES execution changes physical location of computation
- Violates Kerckhoff’s principle assumptions
- Resists:
    - Acoustic attacks
    - Power analysis attacks
    - Timing attacks
    - Execution bypass attacks

---

# 8. AES S-Box Background

F2 = {0,1}  
Addition = XOR  
Multiplication = AND

Polynomial ring:
F2[x]

AES irreducible polynomial:
m(x) = x^8 + x^4 + x^3 + x + 1

Field:
F2[x] / m(x)

---

## Example

p(x) = x^6 + x^4 + x  
q(x) = x^2 + 1

p(x) * q(x) mod m(x) = 1

---

# 9. Lookup Table Problem

- n × 2^n memory required

Examples:
- n = 32 → 137,438,953,472 bits
- n = 64 → 1,180,591,620,717,411,303,424 bits

---

# 10. XOR Circuit

A ⊕ B = (A ∨ B) ∧ ¬(A ∧ B)

---

# 11. Circuit Addition

add_polynomials(r, w):
return [r1 ⊕ w1, r2 ⊕ w2, r3 ⊕ w3, r4 ⊕ w4, r5 ⊕ w5, r6 ⊕ w6, r7 ⊕ w7, r8 ⊕ w8]

---

# 12. Circuit Multiplication

x * p(x) mod m(x)

Polynomial arithmetic over F2[x] / m(x)

---

# 13. Circuit Obfuscation

σ3 swaps when S = 0

Example:

b = 1:
- u = p4
- v = p4 ⊕ p1
- w = p5
- z = p5 ⊕ p1

b = 0:
- u = p5 ⊕ p1
- v = p5
- w = p4 ⊕ p1
- z = p4

---

# 14. Random XOR Circuit

If b = 1:
- z = x ⊕ y
- w = x

If b = 0:
- z = x
- w = x ⊕ y

---

# 15. Moving Computation

- Computation moves unpredictably across circuit
- Controlled by randomness
- Function execution swaps between locations

---

# 16. AES S-Box Obfuscation Complexity

- 7 layers of multiplication
- 7 swaps per layer
- 10 σ3 gates per swap

Total:
7 × 7 × 10 = 490 σ3 gates

---

# 17. General Method

- Functions f and g execute in alternating locations
- Outputs move across circuit
- Execution is not spatially fixed

---

# 18. Summary

- Extends reversible computing
- Introduces self-modifying circuits
- Enables space-time obfuscation of computation
- Applies to AES S-box and general algorithms
- Hinders side-channel and cryptanalysis attacks
- Does not rely on one-way functions

---

# END