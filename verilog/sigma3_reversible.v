// Sigma3 Reversible Gate
// Inputs:  I1, I2, S
// Outputs: O1, O2, S_out
// Behavior:
//   If S=0: swap(I1,I2) -> O1=I2, O2=I1
//   If S=1: pass-through -> O1=I1, O2=I2
// S_out = S always (reversible: S is preserved)

module sigma3_reversible(
    input  wire I1,
    input  wire I2,
    input  wire S,
    output wire O1,
    output wire O2,
    output wire S_out
);
    assign O1    = S ? I1 : I2;
    assign O2    = S ? I2 : I1;
    assign S_out = S;
endmodule

