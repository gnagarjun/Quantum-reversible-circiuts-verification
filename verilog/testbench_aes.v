`timescale 1ns/1ps

module testbench_aes;
    integer i;

    // ---------------------------------------------------------------
    // XOR from sigma3 (Slide 10)
    // ---------------------------------------------------------------
    reg  xor_A, xor_B;
    wire xor_OUT;
    xor_from_sigma dut_xor(.A(xor_A), .B(xor_B), .XOR_OUT(xor_OUT));

    // ---------------------------------------------------------------
    // AES Field Addition 8-bit (Slide 11)
    // ---------------------------------------------------------------
    reg  [7:0] fadd_r, fadd_w;
    wire [7:0] fadd_sum;
    aes_field_add dut_fadd(.r(fadd_r), .w(fadd_w), .sum(fadd_sum));

    // ---------------------------------------------------------------
    // AES Field Multiplication GF(2^8) (Slide 12 + example Slide 8)
    // ---------------------------------------------------------------
    reg  [7:0] fmul_a, fmul_b;
    wire [7:0] fmul_product;
    gf_mul dut_fmul(.a(fmul_a), .b(fmul_b), .product(fmul_product));

    // ---------------------------------------------------------------
    // Obfuscated XOR / Random XOR Circuit (Slide 14)
    // ---------------------------------------------------------------
    reg  ox_x, ox_y, ox_b;
    wire ox_z, ox_w;
    obfuscated_xor dut_ox(.x(ox_x), .y(ox_y), .b(ox_b), .z(ox_z), .w(ox_w));

    // ---------------------------------------------------------------
    // Circuit Obfuscation (Slide 13)
    // ---------------------------------------------------------------
    reg  co_p1, co_p4, co_p5, co_b;
    wire co_u, co_v, co_w, co_z;
    circuit_obfuscation dut_co(
        .p1(co_p1), .p4(co_p4), .p5(co_p5), .b(co_b),
        .u(co_u), .v(co_v), .w(co_w), .z(co_z)
    );

    initial begin
        // === XOR Circuit: all 4 combinations ===
        for (i = 0; i < 4; i = i + 1) begin
            {xor_A, xor_B} = i[1:0]; #10;
            $display("XOR A=%b B=%b XOR_OUT=%b", xor_A, xor_B, xor_OUT);
        end

        // === AES Field Addition: spot tests ===
        // 0x52 + 0x05 = 0x57 (XOR)
        fadd_r = 8'h52; fadd_w = 8'h05; #10;
        $display("FADD r=%02h w=%02h sum=%02h", fadd_r, fadd_w, fadd_sum);
        // 0xFF + 0xFF = 0x00
        fadd_r = 8'hFF; fadd_w = 8'hFF; #10;
        $display("FADD r=%02h w=%02h sum=%02h", fadd_r, fadd_w, fadd_sum);
        // 0xAB + 0x00 = 0xAB
        fadd_r = 8'hAB; fadd_w = 8'h00; #10;
        $display("FADD r=%02h w=%02h sum=%02h", fadd_r, fadd_w, fadd_sum);

        // === AES Field Multiplication: paper example ===
        // p(x) = x^6+x^4+x = 0x52, q(x) = x^2+1 = 0x05 => product = 0x01
        fmul_a = 8'h52; fmul_b = 8'h05; #10;
        $display("FMUL a=%02h b=%02h product=%02h", fmul_a, fmul_b, fmul_product);
        // Additional tests: a * 1 = a
        fmul_a = 8'hAB; fmul_b = 8'h01; #10;
        $display("FMUL a=%02h b=%02h product=%02h", fmul_a, fmul_b, fmul_product);
        // a * 0 = 0
        fmul_a = 8'hAB; fmul_b = 8'h00; #10;
        $display("FMUL a=%02h b=%02h product=%02h", fmul_a, fmul_b, fmul_product);
        // commutativity: 0x53 * 0xCA = ?
        fmul_a = 8'h53; fmul_b = 8'hCA; #10;
        $display("FMUL a=%02h b=%02h product=%02h", fmul_a, fmul_b, fmul_product);
        fmul_a = 8'hCA; fmul_b = 8'h53; #10;
        $display("FMUL a=%02h b=%02h product=%02h", fmul_a, fmul_b, fmul_product);

        // === Obfuscated XOR (Slide 14): all x,y,b combinations ===
        for (i = 0; i < 8; i = i + 1) begin
            {ox_x, ox_y, ox_b} = i[2:0]; #10;
            $display("OXOR x=%b y=%b b=%b z=%b w=%b",
                     ox_x, ox_y, ox_b, ox_z, ox_w);
        end

        // === Circuit Obfuscation (Slide 13): all p1,p4,p5,b combinations ===
        for (i = 0; i < 16; i = i + 1) begin
            {co_p1, co_p4, co_p5, co_b} = i[3:0]; #10;
            $display("COBF p1=%b p4=%b p5=%b b=%b u=%b v=%b w=%b z=%b",
                     co_p1, co_p4, co_p5, co_b,
                     co_u, co_v, co_w, co_z);
        end

        $finish;
    end
endmodule

