// AES Field Addition — Paper Slide 11
// add_polynomials(r, w) = [r1^w1, r2^w2, ..., r8^w8]
// GF(2^8) addition is bit-wise XOR of 8-bit polynomial coefficients.
// Each bit-XOR is built from xor_from_sigma (which uses only sigma3 gates).

module aes_field_add(
    input  wire [7:0] r,
    input  wire [7:0] w,
    output wire [7:0] sum
);
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : xor_bits
            xor_from_sigma bit_xor(
                .A(r[i]),
                .B(w[i]),
                .XOR_OUT(sum[i])
            );
        end
    endgenerate
endmodule
