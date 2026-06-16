`timescale 1ns/1ps

module testbench;
    // sigma3 signals
    reg  s3_I1, s3_I2, s3_S;
    wire s3_O1, s3_O2, s3_S_out;

    // nand signals
    reg  n_A, n_B;
    wire n_NAND_OUT;

    // nor signals
    reg  r_A, r_B;
    wire r_NOR_OUT;

    // self-modifiable signals
    reg  sm_I1, sm_I2, sm_S;
    wire sm_O2, sm_O4;

    integer i;

    // Instantiate modules
    sigma3_reversible dut_sigma3(
        .I1(s3_I1), .I2(s3_I2), .S(s3_S),
        .O1(s3_O1), .O2(s3_O2), .S_out(s3_S_out)
    );

    nand_from_sigma dut_nand(
        .A(n_A), .B(n_B), .NAND_OUT(n_NAND_OUT)
    );

    nor_from_sigma dut_nor(
        .A(r_A), .B(r_B), .NOR_OUT(r_NOR_OUT)
    );

    self_modifiable dut_sm(
        .I1(sm_I1), .I2(sm_I2), .S(sm_S),
        .O2(sm_O2), .O4(sm_O4)
    );

    initial begin
        // === Test sigma3 gate: all 8 combinations ===
        for (i = 0; i < 8; i = i + 1) begin
            {s3_I1, s3_I2, s3_S} = i[2:0];
            #10;
            $display("SIGMA3 I1=%b I2=%b S=%b O1=%b O2=%b S_out=%b",
                     s3_I1, s3_I2, s3_S, s3_O1, s3_O2, s3_S_out);
        end

        // === Test NAND gate: all 4 combinations ===
        for (i = 0; i < 4; i = i + 1) begin
            {n_A, n_B} = i[1:0];
            #10;
            $display("NAND A=%b B=%b NAND_OUT=%b", n_A, n_B, n_NAND_OUT);
        end

        // === Test NOR gate: all 4 combinations ===
        for (i = 0; i < 4; i = i + 1) begin
            {r_A, r_B} = i[1:0];
            #10;
            $display("NOR A=%b B=%b NOR_OUT=%b", r_A, r_B, r_NOR_OUT);
        end

        // === Test self-modifiable circuit ===
        // S=0 and S=1 for all 4 input combos
        for (i = 0; i < 4; i = i + 1) begin
            {sm_I1, sm_I2} = i[1:0];
            sm_S = 0; #10;
            $display("SELFMOD S=%b I1=%b I2=%b O2=%b O4=%b",
                     sm_S, sm_I1, sm_I2, sm_O2, sm_O4);
        end
        for (i = 0; i < 4; i = i + 1) begin
            {sm_I1, sm_I2} = i[1:0];
            sm_S = 1; #10;
            $display("SELFMOD S=%b I1=%b I2=%b O2=%b O4=%b",
                     sm_S, sm_I1, sm_I2, sm_O2, sm_O4);
        end

        $finish;
    end
endmodule

