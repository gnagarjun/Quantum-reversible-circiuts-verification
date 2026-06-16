// AES Field Multiplication — Paper Slide 12
// Implements GF(2^8) multiplication modulo
//   m(x) = x^8 + x^4 + x^3 + x + 1   (AES irreducible polynomial, 0x11B)
//
// xtime(a): multiply a by x in GF(2^8)
//   = (a << 1) XOR 0x1B if bit7 of a was 1
//   = (a << 1)           otherwise
//
// gf_mul(a, b): Russian peasant algorithm
//   Accumulate partial products by conditional xtime.
//
// Paper example (Slide 8):
//   p(x) = x^6 + x^4 + x = 0x52
//   q(x) = x^2 + 1       = 0x05
//   p(x) * q(x) mod m(x) = 1  (they are multiplicative inverses in GF(2^8))

module xtime(
    input  wire [7:0] a,
    output wire [7:0] y
);
    // If MSB set: shift left and XOR with 0x1B (reduction polynomial lower 8 bits)
    assign y = a[7] ? ({a[6:0], 1'b0} ^ 8'h1B) : {a[6:0], 1'b0};
endmodule

// Full GF(2^8) multiplier — combinational
// Uses 8 stages of xtime and conditional XOR accumulation
module gf_mul(
    input  wire [7:0] a,
    input  wire [7:0] b,
    output wire [7:0] product
);
    // a^(2^i) for i=0..7
    wire [7:0] ax [0:7];
    assign ax[0] = a;
    genvar i;
    generate
        for (i = 0; i < 7; i = i + 1) begin : xt_chain
            xtime xt(.a(ax[i]), .y(ax[i+1]));
        end
    endgenerate

    // product = XOR of ax[i] where b[i] == 1
    assign product =
        (b[0] ? ax[0] : 8'h00) ^
        (b[1] ? ax[1] : 8'h00) ^
        (b[2] ? ax[2] : 8'h00) ^
        (b[3] ? ax[3] : 8'h00) ^
        (b[4] ? ax[4] : 8'h00) ^
        (b[5] ? ax[5] : 8'h00) ^
        (b[6] ? ax[6] : 8'h00) ^
        (b[7] ? ax[7] : 8'h00);
endmodule

