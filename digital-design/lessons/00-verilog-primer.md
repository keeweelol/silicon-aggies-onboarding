# Lesson 0 — Verilog in 30 minutes

You need five ideas. That's genuinely it for this block.

---

## The one big idea first

**Verilog is not a programming language.** It looks like C, and that's a trap.

When you write Python, you're writing a list of steps that happen one after another.
When you write Verilog, you're **describing hardware that already exists and is all
running at the same time.** Every line you write is a piece of circuitry that is
permanently there, doing its thing, continuously, in parallel with every other line.

There is no "now do this, then do that." There is only "here is what this wire is
connected to" and "here is what this flip-flop does on every clock tick."

Hold onto that. Most beginner confusion comes from forgetting it.

---

## 1. A module is a box with wires

```verilog
module my_thing (
    input  wire       clk,
    input  wire       a,
    output wire       y
);
    // the guts go here
endmodule
```

A module has a name and a list of ports — the wires going in and out. That's the box.
Everything between `module` and `endmodule` is what's inside it.

**In this block you don't get to choose the ports.** Every Silicon Aggies design uses the
same port list, because it's the pin contract of the actual chip we're taping out:

```verilog
module tt_um_traffic_light (
    input  wire [7:0] ui_in,     // 8 input pins
    output wire [7:0] uo_out,    // 8 output pins
    input  wire [7:0] uio_in,    // 8 more, bidirectional (we don't use them here)
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,       // "you are switched on"
    input  wire       clk,       // the clock
    input  wire       rst_n      // reset. active LOW -- see below
);
```

`[7:0]` means "this is 8 wires bundled together," numbered 7 down to 0. `ui_in[0]` is the
lowest one.

`rst_n` — the `_n` means **active low**. The signal is *normally* 1, and reset happens
when it goes to **0**. This trips up everybody once. It's a real hardware convention, not
us being difficult.

---

## 2. `wire` versus `reg`

Two ways to hold a value.

**`wire`** is a piece of metal. It doesn't remember anything. Whatever is driving it right
now is what it is. You drive a wire with `assign`:

```verilog
wire alarm;
assign alarm = too_hot | too_loud;    // alarm is ALWAYS this. Continuously. Forever.
```

That `assign` is not an action that happens once. It's a permanent connection. If
`too_hot` changes, `alarm` changes, instantly, with no clock involved.

**`reg`** is something that can remember — usually a flip-flop. You drive it inside an
`always` block:

```verilog
reg [3:0] count;

always @(posedge clk) begin
    count <= count + 1;
end
```

The name `reg` is honestly a bad name and it confuses everyone. Just remember: **if you
assign to it inside an `always` block, it has to be declared `reg`.**

---

## 3. `always @(posedge clk)` is where memory lives

```verilog
always @(posedge clk) begin
    // this happens once per rising clock edge
end
```

Read it as: "on every rising edge of the clock, do this." That's how you build anything
that remembers — a counter, a state machine, anything that has to know what happened last
tick.

Add reset like this:

```verilog
always @(posedge clk) begin
    if (!rst_n) begin
        count <= 0;              // reset: force it to a known value
    end else begin
        count <= count + 1;      // normal operation
    end
end
```

`!rst_n` means "rst_n is 0," which is when reset is happening. Read it out loud as "if
not-reset-n" or just "if we're being reset."

---

## 4. `<=` versus `=` — the rule that will save you an hour

Inside `always @(posedge clk)`, **always use `<=`. Never use `=`.**

`<=` is called a nonblocking assignment. It means "at the next clock edge, this becomes
that." All of the `<=` in a block happen simultaneously, using the values from *before*
the edge.

Here's why it matters:

```verilog
always @(posedge clk) begin
    b <= a;
    c <= b;
end
```

With `<=`, `c` gets the **old** `b` — the value from before this clock edge. That's two
flip-flops in a row, a shift register. Correct.

With `=`, `c` would get the **new** `b`, which is `a`. One flip-flop, and `b` and `c` are
just copies. Not what you drew, not what you wanted, and it can even simulate differently
than it behaves in real silicon.

**The rule: `<=` inside `always @(posedge clk)`. Don't think about it, just do it.**

---

## 5. `case` for state machines

A `case` statement picks one branch based on a value:

```verilog
case (state)
    S_GREEN:  begin
        // what to do while green
    end
    S_YELLOW: begin
        // what to do while yellow
    end
    S_RED: begin
        // what to do while red
    end
    default: begin
        // catch-all: anything not listed above
    end
endcase
```

**Always include a `default`.** In simulation it barely matters. In real silicon, a
circuit can end up in a state you never intended, and without a `default` it can sit there
stuck forever with no way out. Point it back at a safe state.

---

## Two more things you'll see

**`localparam`** is a named constant. Use them instead of scattering magic numbers:

```verilog
localparam GREEN_TIME = 12;
localparam S_GREEN    = 2'b00;
```

`2'b00` means "a 2-bit binary value, `00`." The format is *width* `'` *base* *value*.
So `8'd255` is 8 bits, decimal, 255. `4'hF` is 4 bits, hex, F.

**Comparisons** work like you'd expect: `==`, `!=`, `<`, `>=`. Logic operators are `&&`
(and), `||` (or), `!` (not) for single true/false values, and `&`, `|`, `~` when you're
operating on every bit of a bundle.

---

## That's the whole language, for now

Really. There's a lot more Verilog, but those five ideas cover everything in this block
and most of what you'll write in the next two.

**One habit to start right now:** when you write a line, ask yourself *what hardware is
this?* `assign y = a & b;` is an AND gate — a physical thing with two inputs and one
output that exists on the chip. `count <= count + 1;` is a register plus an adder. If you
can't answer what a line builds, that line is probably wrong.

---

**Next:** [Lesson 1 — Your first simulation](01-first-simulation.md). Time to actually run
something.
