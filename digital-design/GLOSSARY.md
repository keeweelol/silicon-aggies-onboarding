# Glossary

Every term used in this block, in plain language.

---

**Active low** — a signal that means "do the thing" when it is 0, not 1. Written with an
`_n` suffix, like `rst_n`. Reset happens when `rst_n` is 0.

**`always @(posedge clk)`** — a block of Verilog that runs once on every rising edge of
the clock. This is where anything that remembers a value lives.

**Blocking / nonblocking (`=` / `<=`)** — two kinds of assignment. Inside a clocked block,
always use `<=`. See [Lesson 0](lessons/00-verilog-primer.md).

**Clock** — a signal that alternates 0,1,0,1 forever, at a fixed rate. It's the heartbeat
everything in a synchronous design moves to.

**Combinational logic** — logic with no memory. The output depends only on the inputs
right now. An AND gate is combinational. `assign` describes combinational logic.

**Edge / rising edge / posedge** — the moment a signal goes from 0 to 1. Flip-flops
capture their input at that instant.

**FSM (finite state machine)** — hardware that is always in exactly one of a small set of
states and moves between them based on conditions. See [Lesson 2](lessons/02-state-machines.md).

**Flip-flop** — the basic memory element. Holds one bit, updates on the clock edge.

**GTKWave** — the program that displays waveforms from a `.vcd` file.

**Icarus Verilog (`iverilog`)** — the simulator. Compiles your Verilog and runs it.

**Latch (as a verb)** — to capture a brief signal and hold it until you can act on it.
What you do with the pedestrian button.

**`localparam`** — a named constant. `localparam GREEN_TIME = 12;`

**One-hot** — a set of signals where exactly one is high at a time. Your three lights are
one-hot.

**PDK (process design kit)** — the files a foundry provides describing what you're allowed
to build in their process. We use sky130. Comes up in Block 3, not this one.

**Pin contract** — the fixed port list every Silicon Aggies design uses (`ui_in`,
`uo_out`, `uio_*`, `clk`, `rst_n`, `ena`). It's the Tiny Tapeout interface.

**Pulse** — a signal that goes high for a short time (here, one clock tick) and returns
low.

**`reg`** — a Verilog type for something assigned inside an `always` block. Usually
becomes a flip-flop. Badly named; don't read too much into it.

**Reset** — forcing the design into a known starting state. Ours is synchronous (it takes
effect on a clock edge) and active low.

**RTL (register transfer level)** — the style of Verilog you're writing: describing
hardware in terms of registers and the logic between them.

**Sequential logic** — logic with memory, driven by a clock. The opposite of
combinational.

**Simulation** — running your design in software to see what it would do, before any
hardware exists.

**Synchronous** — everything happens on clock edges. What we do.

**Synthesis** — turning your Verilog into actual logic gates. Happens in Block 3.

**Testbench** — code that drives your design with inputs and checks the outputs. Not part
of the chip; it exists only in simulation. We give you one this block; you write one in
Block 2.

**Tick** — one clock cycle. We measure the traffic light's timing in ticks.

**Tiny Tapeout** — the shared manufacturing run we submit to. Many small designs on one
chip.

**`.vcd` (value change dump)** — the file a simulation writes recording every signal at
every moment. GTKWave reads it.

**Waveform** — the picture of signals over time. How you actually debug hardware.

**`wire`** — a Verilog type for a plain connection with no memory. Driven with `assign`.
