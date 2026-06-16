// Self-Modifiable Circuit using sigma3
// Paper claim:
//   When S=1: O4 = NOR(I1,I2), O2 = NAND(I1,I2)
//   When S=0: O4 = NAND(I1,I2), O2 = NOR(I1,I2)
//
// Implementation:
//   Compute NAND and NOR internally, then use sigma3 to swap
//   based on control signal S.

module self_modifiable(
    input  wire I1,
    input  wire I2,
    input  wire S,
    output wire O2,
    output wire O4
);
    wire nand_result, nor_result;
    wire O1_sigma, O2_sigma, S_out_sigma;

    // Compute NAND(I1,I2)
    nand_from_sigma nand_inst(
        .A(I1),
        .B(I2),
        .NAND_OUT(nand_result)
    );

    // Compute NOR(I1,I2)
    nor_from_sigma nor_inst(
        .A(I1),
        .B(I2),
        .NOR_OUT(nor_result)
    );

    // Use sigma3 to swap outputs based on S:
    //   S=0: swap -> O1=nor_result(->O4), O2=nand_result
    //          meaning O4=NOR (from swap position O1), O2=NAND (from swap position O2)
    //   Wait, per paper:
    //     S=0: O4=NAND, O2=NOR
    //     S=1: O4=NOR,  O2=NAND
    // Feed nand_result as I1, nor_result as I2 into sigma3:
    //   S=0 (swap): O1=nor_result, O2=nand_result  -> assign O4=O1=nor? No...
    // Let's feed nor_result as I1, nand_result as I2:
    //   S=0 (swap): O1=nand_result, O2=nor_result  -> O4=O1=NAND, O2=NOR ✓
    //   S=1 (pass): O1=nor_result,  O2=nand_result -> O4=O1=NOR,  O2=NAND ✓

    sigma3_reversible swap_inst(
        .I1(nor_result),
        .I2(nand_result),
        .S(S),
        .O1(O4),
        .O2(O2),
        .S_out(S_out_sigma)
    );
endmodule

