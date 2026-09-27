# Lesson 0: Testbenches in 30 minutes

This lesson covers two things: the small differences between the Verilog you wrote in
Block 1 and the SystemVerilog in this block, and what goes inside a testbench. Just read
for now. You'll run everything in Lesson 1.

---

## Part 1: SystemVerilog, compared to Verilog

SystemVerilog is a newer version of Verilog. Everything you learned in Block 1 still works.
The designs in this block use three new things.

### `logic` instead of `wire` and `reg`

In Block 1 you had to decide between `wire` and `reg`. SystemVerilog has `logic`, which
works for both. You'll see it everywhere in this block:

```systemverilog
logic       clk;      // one bit
logic [3:0] count;    // four bits, numbered 3 down to 0
```

### `always_ff` instead of `always`

```systemverilog
always_ff @(posedge clk) begin
    count <= count + 1'b1;
end
```

It means the same thing as `always @(posedge clk)`. The `_ff` tells the tools "this block
should build flip-flops," so they can warn you if it wouldn't.

### The `.sv` file extension

SystemVerilog files end in `.sv` instead of `.v`.

That's everything new in the designs. The rest is the Verilog you already know.

---

## Part 2: What a testbench is

A **testbench** is a module whose only job is to test another module. It creates the design,
wiggles its inputs, and records what comes out. It never becomes part of the chip. It only
exists in simulation.

The module being tested is called the **DUT**, short for "design under test."

Think of it like a lab bench. The DUT is the circuit clamped down in the middle. The
testbench is everything around it: the power supply, the function generator feeding it a
clock, your hands flipping switches, and the oscilloscope recording what happens.

Every testbench in this block has the same five parts. Here's the golden counter's
testbench, cut down so you can see them:

```systemverilog
`timescale 1ns/1ps

module test();                        // a testbench has no ports

    // PART 1: one signal for each port on the DUT
    logic clk;
    logic rst_n;
    logic en;
    logic [3:0] count;

    // PART 2: the DUT itself, with every port connected
    counter dut(
        .clk(clk),
        .rst_n(rst_n),
        .en(en),
        .count(count)
    );

    // PART 3: a clock
    initial clk = 0;
    always #10 clk = ~clk;

    // PART 4 and PART 5: the test steps, then stop
    initial begin
        $dumpfile("dump.vcd");        // record a waveform into this file
        $dumpvars(0, test);           // record every signal in the testbench

        rst_n = 0;                    // hold reset
        en = 0;
        repeat (2) @(posedge clk);    // for two clock edges

        @(negedge clk);
        rst_n = 1;                    // let go of reset
        en = 1;                       // start counting
        repeat (10) @(posedge clk);   // for ten clock edges

        $finish;                      // PART 5: stop the simulation
    end
endmodule
```

Now each part, one at a time.

### `timescale 1ns/1ps`

The first line sets the units for time. `#10` will mean 10 nanoseconds. You can copy this
line as-is into every testbench.

### `module test();`

The testbench is a module like any other, but with an empty port list, because nothing is
outside it. In this block every testbench is named `test`. The commands in the lessons
depend on that name.

### Part 1: signals

One `logic` for each port on the DUT, with the same width. If the DUT has
`output logic [3:0] count`, the testbench needs `logic [3:0] count;`.

### Part 2: the DUT

```systemverilog
counter dut(
    .clk(clk),
    .rst_n(rst_n),
    ...
);
```

This line creates one copy of the `counter` module and names it `dut`. Creating a copy of
a module inside another is called **instantiating** it, and the copy is an **instance**.

Each `.clk(clk)` connects one port. Read it as "the counter's `clk` port, connected to my
`clk` signal." The name after the dot is the port on the DUT. The name in the parentheses
is the testbench's signal. Here they happen to be the same, which keeps things simple.

Separate the connections with commas. The last one has no comma after it.

### Part 3: the clock

```systemverilog
initial clk = 0;
always #10 clk = ~clk;
```

`initial` runs once, at time zero. So the clock starts at 0.

`always #10 clk = ~clk;` means "every 10 ns, flip the clock." It goes 0 for 10 ns, 1 for
10 ns, and so on, forever. One full clock period is 20 ns.

### Part 4: the test steps

This is the part you write. It's an `initial begin ... end` block that runs from top to
bottom, once. Unlike design code, testbench code **does** run in order, like a program.

You'll only need a few commands:

| You write | It means |
|---|---|
| `rst_n = 0;` | Set an input. In testbench code, use `=`, not `<=`. |
| `@(posedge clk);` | Wait until the next rising clock edge. |
| `@(negedge clk);` | Wait until the next falling clock edge. |
| `repeat (5) @(posedge clk);` | Wait for five rising edges. |
| `#10;` | Wait 10 ns. |

A `for` loop repeats a few lines. You'll need one in Lesson 4:

```systemverilog
for (int i = 0; i < 16; i++) begin
    // these lines run 16 times, with i = 0, 1, 2, ... 15
end
```

### Change inputs on the falling edge

Look at the example again:

```systemverilog
@(negedge clk);
rst_n = 1;
```

The DUT's flip-flops grab their inputs on the **rising** edge. If the testbench changed an
input at that exact same instant, it would be a race: does the flip-flop see the old value
or the new one? The answer depends on the simulator, and you'd get confusing results.

So change inputs on the **falling** edge, halfway between two rising edges. By the next
rising edge the input has been steady for half a clock, and there's no question which value
the DUT sees. Every testbench in this block does this. Copy the habit.

### Part 5: `$dumpfile`, `$dumpvars`, and `$finish`

- `$dumpfile("dump.vcd");` names the waveform file.
- `$dumpvars(0, test);` records every signal inside `test`, including the ones inside the
  DUT.
- `$finish;` stops the simulation. **Without it, the clock runs forever and so does the
  simulation.**

---

## Part 3: What "testing against a spec" means

A **spec** is a numbered list of exactly what a design is supposed to do. Here's the spec for
the counter in this block:

1. When `rst_n` is 0 on a rising clock edge, `count` becomes 0.
2. When `rst_n` is 1 and `en` is 1, `count` goes up by one on every rising edge.
3. When `en` is 0, `count` stays the same.
4. Counting up from 15 goes back to 0.

Testing a design means making every line of the spec happen in simulation, and checking
that the design does what that line says. If a spec line never happens in your testbench,
you haven't tested it, even if everything you did test looks fine.

In this block, you'll check by looking at the waveform. Real verification teams write
testbenches that check themselves, and there's a stretch goal in Lesson 2 that gets you
started on that.

---

**Next:** [Lesson 1: Run the golden counter](01-golden-counter.md).
