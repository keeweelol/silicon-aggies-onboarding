// Extra stimulus for the automatic PR check (not part of any lesson).
// Drives the counter-SRAM with pseudo-random en, write_en, write_data and
// occasional resets for 400 clocks. The check compares the result against
// the golden counter-SRAM.
`timescale 1ns/1ps

module test();
	logic clk;
	logic rst_n;
	logic en;
	logic write_en;
	logic [7:0] write_data;
	logic [3:0] address;
	logic [7:0] read_data;

	counter_sram dut(
		.clk(clk),
		.rst_n(rst_n),
		.en(en),
		.write_en(write_en),
		.write_data(write_data),
		.address(address),
		.read_data(read_data)
	);

	initial clk = 0;
	always #10 clk = ~clk;

	logic [15:0] lfsr;

	initial begin
		$dumpfile("dump.vcd");
		$dumpvars(0, test);
		lfsr = 16'hBEEF;
		rst_n = 0;
		en = 0;
		write_en = 0;
		write_data = 8'h00;
		repeat (2) @(posedge clk);
		// fill every slot first, so the reads below never see an unwritten slot
		@(negedge clk);
		rst_n = 1;
		en = 1;
		write_en = 1;
		for (int i = 0; i < 16; i++) begin
			write_data = 8'd100 + i[7:0];
			@(posedge clk);
			@(negedge clk);
		end
		for (int i = 0; i < 400; i++) begin
			lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
			en = (lfsr[1:0] != 2'd0);
			write_en = lfsr[3];
			write_data = lfsr[15:8];
			rst_n = (lfsr[10:5] != 6'd0);
			@(posedge clk);
			@(negedge clk);
		end
		$finish;
	end
endmodule
