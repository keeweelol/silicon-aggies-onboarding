// counter module that increments the address of the SRAM
// cell each time the count increases
// when the reset is active, the SRAM will return to the first memory address as the count resets

`timescale 1ns/1ps

// 4-bit counter module
module counter (
	input logic clk,
	input logic rst_n,
	input logic en,
	output logic [3:0] count
);

	always_ff @(posedge clk) begin
		// check reset signal first
		if (!rst_n) begin
			count <= 4'd0;
		end
		else if (en) begin
			count <= count + 1'b1;
		end
	end

endmodule

// SRAM module
module SRAM (
	input logic clk,
	input logic write_en,
	input logic [3:0] address,
	input logic [7:0] write_data,
	output logic [7:0] read_data
);

	// instantiate a memory array with 16 addresses each storing 8 bits
	logic [7:0] memory [0:15];

	always_ff @(posedge clk) begin
		if (write_en) begin
			memory[address] <= write_data;
		end
		read_data <= memory[address];
	end
endmodule

// top level module connecting counter and SRAM
module counter_sram (
	// count will not be declared here because it is an internal signal of the counter
	input logic clk,
	input logic rst_n,
	input logic en,
	input logic write_en,
	input logic [7:0] write_data,
	output logic [3:0] address,
	output logic [7:0] read_data
);

	// instantiations of the previous modules
	counter counter_instance (
		.clk(clk),
		.rst_n(rst_n),
		.en(en),
		.count(address)	// the count from the counter will correlate to the address of the SRAM
						// 1 correlates to address 1 so on and so forth...
	);

	SRAM SRAM_instance (
		.clk(clk),
		.write_en(write_en),
		.address(address),
		.write_data(write_data),
		.read_data(read_data)
	);
	
endmodule
