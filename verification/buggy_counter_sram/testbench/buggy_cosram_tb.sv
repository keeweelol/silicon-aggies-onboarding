`timescale 1ns/1ps

module test();

	// declare inputs and outputs from top level module (counter_sram)
	logic clk;
	logic rst_n;
	logic en;
	logic write_en;
	logic [7:0] write_data;
	logic [3:0] address;
	logic [7:0] read_data;

	// EXERCISE TASK #1
	// Create a counter_sram named dut and connect all seven of its ports.
	// In .clk(clk), the name after the dot is the design's port and the
	// name in the parentheses is this testbench's signal.

	// set initial signal values
	initial clk = 0;
	initial rst_n = 0;
	initial en = 0;
	initial write_en = 0;
	initial write_data = 8'h00;

	always #10 clk = ~clk;

	// begin test cases
	initial begin
		$dumpfile("dump.vcd");
		$dumpvars(0, test);		

		repeat (2) @(posedge clk); // wait until two rising clk edges are met before continuing

		// change inputs away from rising edge
		@(negedge clk);
		rst_n = 1;
		en = 1;
		write_en = 1;

		// EXERCISE TASK #2
		// Write a value into each of the 16 memory addresses.
		// Use a for loop: set write_data, wait for a rising edge, then a falling edge.

		
		write_en = 0; // disable writing

		repeat (16) @(posedge clk); // wait for 16 rising clk edges to view written data
		$finish;
	end
endmodule
