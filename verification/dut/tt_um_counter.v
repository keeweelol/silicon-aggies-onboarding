`default_nettype none

module tt_um_counter (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    wire [7:0] load_value = ui_in;
    wire       en   = uio_in[0];
    wire       load = uio_in[1];

    reg [7:0] count;

    always @(posedge clk) begin
        if (!rst_n) begin
            count <= 8'h00;
        end else if (en) begin
            if (count != 8'hFF)
                count <= count + 8'd1;
        end else if (load) begin
            count <= load_value;
        end
    end

    assign uo_out  = count;
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
    wire _unused = &{ena, uio_in[7:2], 1'b0};
endmodule
