// testbench to test the functionality of 4-bit counter
`timescale 1ns/1ps

module test();

	// inputs and outputs
	logic clk; // clock signal
	logic rst_n; // active low reset
	logic en; // enable signal
	logic [3:0] count;

	// instantiate a counter and map all variables
	counter dut(
		.clk(clk),
		.rst_n(rst_n),
		.en(en),
		.count(count)
	);

	// initialize clock and reset to 0
	// clock toggles every 10 ns, so one full clock period is 20 ns
	initial clk = 0;
	initial rst_n = 0;
	initial en = 0;
	always #10 clk = ~clk;

	initial begin
		// dumpfile to view signals
		$dumpfile("dump.vcd");
		// dump all signals in the test bench
		$dumpvars(0, test);

		// test cases

		// 1. hold reset low for two rising clock edges so count starts at a known 0
		//    (without this, count starts as x, meaning unknown, in most simulators)
		repeat (2) @(posedge clk);

		// change inputs on the falling edge so they are stable before the next rising edge
		@(negedge clk);
		rst_n = 1;

		// 2. enable the counter and let it count for 20 cycles
		//    (4 bits only goes up to 15, so watch it wrap back around to 0)
		en = 1;
		repeat (20) @(posedge clk);

		// 3. disable the counter: count should hold its value
		@(negedge clk);
		en = 0;
		repeat (4) @(posedge clk);

		// 4. re-enable, then pull reset low mid-count: count should go back to 0
		@(negedge clk);
		en = 1;
		repeat (3) @(posedge clk);
		@(negedge clk);
		rst_n = 0;
		repeat (2) @(posedge clk);

		$finish; // explicitly end simulation
	end
endmodule
