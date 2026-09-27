`timescale 1ns/1ps

module counter (
	input logic clk,
	input logic rst_n,
	input logic en,
	output logic [3:0] count
);

	always_ff @(posedge clk) begin
		// check the reset signal first
		if (!rst_n) begin
			count <= 4'd0;
		end
		// check if we are enabling the counter to increment
		else if (en) begin
			// if the enable signal is high, increment count
			count <= count + 1'b1;
		end
	end

endmodule
