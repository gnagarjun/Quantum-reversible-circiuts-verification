// XOR gate constructed from sigma3-based NAND/NOR gates
// Paper (Slide 10): A ⊕ B = (A ∨ B) ∧ ¬(A ∧ B)
//
// Implementation using only NAND gates (all from sigma3):
//   Let N = NAND(A, B)
//   XOR = NAND(NAND(A, N), NAND(B, N))
// This is the classic 4-NAND XOR, where every NAND is built from sigma3.

module xor_from_sigma(
    input  wire A,
    input  wire B,
    output wire XOR_OUT
);
    wire N;       // NAND(A,B)
    wire AN;      // NAND(A, N)
    wire BN;      // NAND(B, N)

    // N = NAND(A,B)
    nand_from_sigma g1(.A(A),  .B(B),  .NAND_OUT(N));
    // AN = NAND(A, N)
    nand_from_sigma g2(.A(A),  .B(N),  .NAND_OUT(AN));
    // BN = NAND(B, N)
    nand_from_sigma g3(.A(B),  .B(N),  .NAND_OUT(BN));
    // XOR = NAND(AN, BN)
    nand_from_sigma g4(.A(AN), .B(BN), .NAND_OUT(XOR_OUT));
endmodule

