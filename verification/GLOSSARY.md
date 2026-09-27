# Glossary (Block 2)

New terms from this block, in plain language. For Block 1 terms like clock, flip-flop, and
reset, see the [Block 1 glossary](../digital-design/GLOSSARY.md).

---

**Address:** the number of a slot in a memory. The SRAM in this block has 16 slots, so the
addresses go from 0 to 15.

**`always_ff`:** SystemVerilog's version of `always` for clocked logic. It means the same as
`always @(posedge clk)`, and tells the tools this block should build flip-flops.

**Bug:** a place where the design doesn't do what the spec says.

**Buggy version:** a copy of a design with bugs planted on purpose, so you can practice
finding them.

**`diff`:** a terminal command that prints the lines that differ between two files.

**DUT (design under test):** the module a testbench is testing.

**`$dumpfile` and `$dumpvars`:** testbench commands that record signals into a waveform file
(`dump.vcd`).

**`$finish`:** a testbench command that ends the simulation.

**Golden version:** a copy of a design that is known to work. You compare against it.

**Instance, instantiate:** creating a copy of one module inside another is called
instantiating it. The copy is an instance. `counter dut(...)` makes an instance of `counter`
named `dut`.

**`logic`:** SystemVerilog's signal type. It replaces both `wire` and `reg`.

**`obj_dir`:** the folder Verilator creates when it builds your simulation. The program
inside it is `obj_dir/Vtest`. Never commit it to git.

**Port connection:** the `.clk(clk)` lines in an instance. The name after the dot is the
DUT's port. The name in the parentheses is the testbench's signal.

**Read data:** the value coming out of a memory.

**Root cause:** the actual line of code that makes a bug happen. Compare with *symptom*.

**Spec (specification):** the exact, numbered list of what a design is supposed to do.
You test against the spec, not against what the code happens to do.

**SRAM (static random-access memory):** a small, fast memory made of flip-flop-like cells.
You write a value into a numbered slot and read it back later.

**Symptom:** what a bug looks like from the outside, like "`count` gets stuck at 5." Compare
with *root cause*.

**SystemVerilog:** a newer version of Verilog. It adds `logic`, `always_ff`, and many other
features. Files end in `.sv`.

**Testbench:** a module that creates a DUT, drives its inputs, and records or checks its
outputs. It only exists in simulation.

**`timescale`:** the line at the top of a testbench that sets the time units, so `#10` means
10 nanoseconds.

**Top-level module:** the outermost module in a design, the one that holds all the others.
In the counter-SRAM, that's `counter_sram`.

**Verilator:** the simulator this block uses. It turns your SystemVerilog into a C++ program,
compiles it, and gives you a program you run to simulate.

**Warning:** a message from a tool about something that might be wrong. Verilator stops on
warnings by default, so you have to fix them.

**Width:** how many bits a signal has. `logic [7:0] write_data` is 8 bits wide. Assigning a
wider value to a narrower signal causes a width warning.

**Write enable:** a signal that says "store the data now." When `write_en` is 1 on a rising
edge, the memory saves `write_data` at the current address.

**`x`:** "unknown" in a simulator. A signal shows `x` when nothing has set it yet. Icarus
shows `x`. Verilator doesn't; it starts everything at 0.
