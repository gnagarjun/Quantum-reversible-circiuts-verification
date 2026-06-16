// Random XOR Circuit — Paper Slide 14
//
// A sigma3-based circuit where control bit b determines
// WHICH output wire receives the XOR result:
//
//   b = 1:  z = x ⊕ y,  w = x
//   b = 0:  z = x,      w = x ⊕ y
//
// Implementation:
//   Compute xor_xy = x ⊕ y
//   Feed sigma3(xor_xy, x, b):
//     b=1 (pass): O1=xor_xy → z=x⊕y,  O2=x → w=x     ✓
//     b=0 (swap): O1=x      → z=x,     O2=xor_xy → w=x⊕y ✓
//
// This is the fundamental building block of "moving computation":
// the XOR result unpredictably moves between output locations.

module obfuscated_xor(
    input  wire x,
    input  wire y,
    input  wire b,       // control: 1=pass, 0=swap
    output wire z,       // location 1
    output wire w        // location 2
);
    wire xor_xy;
    wire S_out;

    // XOR from sigma3-based NAND gates
    xor_from_sigma xg(.A(x), .B(y), .XOR_OUT(xor_xy));

    // sigma3 routes xor result based on b
    sigma3_reversible route(
        .I1(xor_xy),
        .I2(x),
        .S(b),
        .O1(z),
        .O2(w),
        .S_out(S_out)
    );
endmodule

