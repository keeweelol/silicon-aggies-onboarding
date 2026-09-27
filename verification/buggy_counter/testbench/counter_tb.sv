// Testbench for the buggy 4-bit counter.
// You fill this in during Block 2, Lesson 2. Follow the lesson step by step.
// Lesson 0 explains every part of a testbench if you get stuck.

`timescale 1ns/1ps

module test();

	// ===============================================================
	// PART 1: signals
	// TODO: declare one logic signal for each port of the counter:
	//       clk, rst_n, en (1 bit each) and count (4 bits: logic [3:0] count;)
	// ===============================================================


	// ===============================================================
	// PART 2: the design under test
	// TODO: create a counter named dut and connect all four ports by name,
	//       like this:  .clk(clk),
	// ===============================================================


	// ===============================================================
	// PART 3: the clock (done for you)
	// Starts at 0 and flips every 10 ns, so one clock period is 20 ns.
	// ===============================================================
	initial clk = 0;
	always #10 clk = ~clk;

	// ===============================================================
	// PART 4: the test steps
	// ===============================================================
	initial begin
		$dumpfile("dump.vcd");	// the waveform file
		$dumpvars(0, test);	// record every signal

		// TODO step A: hold reset for two clock edges

		// TODO step B: release reset, turn on en, and count for 20 edges

		// TODO step C: turn en off for 4 edges

		// TODO step D: turn en back on for 3 edges, then pull reset low for 2 edges

		$finish;	// PART 5: stop the simulation
	end

endmodule
