// Circuit Obfuscation — Paper Slide 13
//
// Demonstrates how sigma3 routes polynomial computation results
// to different physical locations based on control bit b.
//
// Given polynomial coefficients p1, p4, p5:
//   Compute:  xor_p4_p1 = p4 ⊕ p1
//             xor_p5_p1 = p5 ⊕ p1
//
//   b = 1 (pass-through):
//       u = p4,      v = p4 ⊕ p1,   w = p5,      z = p5 ⊕ p1
//
//   b = 0 (swap):
//       u = p5 ⊕ p1, v = p5,        w = p4 ⊕ p1, z = p4
//
// Implementation uses 2 sigma3 gates:
//   Gate 1: sigma3(p4, xor_p5_p1, b)   → (u, z)
//   Gate 2: sigma3(xor_p4_p1, p5, b)   → (v, w)
//
// The computation (XOR results) physically moves between u/z and v/w
// without any change to connections — pure sigma3 routing.

module circuit_obfuscation(
    input  wire p1,    // polynomial coefficient 1
    input  wire p4,    // polynomial coefficient 4
    input  wire p5,    // polynomial coefficient 5
    input  wire b,     // control bit: 1=pass, 0=swap
    output wire u,
    output wire v,
    output wire w,
    output wire z
);
    wire xor_p4_p1, xor_p5_p1;
    wire S_out1, S_out2;

    // Compute XOR combinations
    xor_from_sigma xg1(.A(p4), .B(p1), .XOR_OUT(xor_p4_p1));
    xor_from_sigma xg2(.A(p5), .B(p1), .XOR_OUT(xor_p5_p1));

    // Gate 1: routes p4 and xor_p5_p1 based on b → outputs u and z
    sigma3_reversible g1(
        .I1(p4),         .I2(xor_p5_p1),
        .S(b),
        .O1(u),          .O2(z),
        .S_out(S_out1)
    );

    // Gate 2: routes xor_p4_p1 and p5 based on b → outputs v and w
    sigma3_reversible g2(
        .I1(xor_p4_p1),  .I2(p5),
        .S(b),
        .O1(v),          .O2(w),
        .S_out(S_out2)
    );
endmodule

