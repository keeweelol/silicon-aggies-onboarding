# Buggy counter (Lesson 2)

The same 4-bit counter as `golden_counter`, with **two bugs** planted in it. You finish the
testbench, find the bugs in the waveform, and fix them.

**Instructions:** [Lesson 2: Find the bugs in the counter](../lessons/02-buggy-counter.md)

Don't work in this folder. Copy it into your submission folder first (Lesson 2, Step 1).
The original stays here so you can prove your testbench catches the bugs at the end.

| File | What it is |
|---|---|
| `buggy_design/counter.sv` | the counter, with two bugs |
| `testbench/counter_tb.sv` | a testbench outline with TODOs for you to fill in |

Try to find the bugs without looking at `golden_counter`. If you're stuck, use the hints in
the lesson, then look at the golden version before you ask an AI.

Build, run, and look, from inside your copy:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &    # Ubuntu / Windows
surfer dump.vcd &     # Mac
```

Exercise by Bryson Fields. Questions: the ASIC GroupMe, or email Bryson Fields
(bafields1@aggies.ncat.edu) or Zachary Johnson (zejohnson3@aggies.ncat.edu).
