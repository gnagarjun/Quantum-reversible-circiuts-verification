// NOR gate constructed from sigma3 reversible gate
// Approach:
//   NOR(A,B) = NOT(A) AND NOT(B)
//   Apply sigma3 with I1=~A, I2=~B, S=~A:
//     O2 = AND(~A, ~B) = NOR(A,B)
//   So NOR_OUT = O2 directly (no extra NOT needed)

module nor_from_sigma(
    input  wire A,
    input  wire B,
    output wire NOR_OUT
);
    wire nA, nB;
    wire O1, O2, S_out;

    assign nA = ~A;
    assign nB = ~B;

    // sigma3(~A, ~B, S=~A) -> O2 = AND(~A,~B) = NOR(A,B)
    sigma3_reversible g1(
        .I1(nA),
        .I2(nB),
        .S(nA),
        .O1(O1),
        .O2(O2),
        .S_out(S_out)
    );

    assign NOR_OUT = O2;
endmodule

