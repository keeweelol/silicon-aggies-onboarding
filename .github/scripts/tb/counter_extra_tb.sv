// Extra stimulus for the automatic PR check (not part of any lesson).
// Drives the counter with pseudo-random en and occasional resets for 300
// clocks. The check compares the result against the golden counter, so a
// "fix" that only works for the lesson's testbench still gets caught.
`timescale 1ns/1ps

module test();
	logic clk;
	logic rst_n;
	logic en;
	logic [3:0] count;

	counter dut(
		.clk(clk),
		.rst_n(rst_n),
		.en(en),
		.count(count)
	);

	initial clk = 0;
	always #10 clk = ~clk;

	logic [15:0] lfsr;

	initial begin
		$dumpfile("dump.vcd");
		$dumpvars(0, test);
		lfsr = 16'hACE1;
		rst_n = 0;
		en = 0;
		repeat (2) @(posedge clk);
		for (int i = 0; i < 300; i++) begin
			@(negedge clk);
			lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
			en = (lfsr[2:0] != 3'd0);       // mostly counting, sometimes paused
			rst_n = (lfsr[9:4] != 6'd0);    // a reset now and then
		end
		$finish;
	end
endmodule
