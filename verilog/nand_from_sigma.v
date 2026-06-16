// NAND gate constructed from sigma3 reversible gate
// Approach:
//   sigma3(A, B, S=A): when S=A,
//     if A=0: swap -> O1=B, O2=A=0   => O2=0=A&B (correct)
//     if A=1: pass -> O1=A=1, O2=B   => O2=B=A&B (correct)
//   So O2 = AND(A,B)
//   NAND(A,B) = NOT(AND(A,B)) = NOT(O2)
//
// Ancilla output O1 is discarded (garbage output).

module nand_from_sigma(
    input  wire A,
    input  wire B,
    output wire NAND_OUT
);
    wire O1, O2, S_out;
    // Use sigma3 with S=A to compute AND in O2
    sigma3_reversible g1(
        .I1(A),
        .I2(B),
        .S(A),
        .O1(O1),
        .O2(O2),
        .S_out(S_out)
    );
    // NAND = NOT(AND) = NOT(O2)
    assign NAND_OUT = ~O2;
endmodule

