# Buggy counter-SRAM (Lesson 4)

The same counter-SRAM as `golden_counter_sram`, with **three bugs** planted in it, and a
testbench with two parts left for you to write.

**Instructions:** [Lesson 4: Find the bugs in the counter-SRAM](../lessons/04-buggy-counter-sram.md)

Don't work in this folder. You copied it into your submission folder in Lesson 2, Step 1.
The original stays here so you can prove your testbench catches the bugs at the end.

| File | What it is |
|---|---|
| `buggy_design/counter_sram.sv` | the counter-SRAM, with three bugs |
| `testbench/buggy_cosram_tb.sv` | a testbench with `EXERCISE TASK #1` and `#2` for you to finish |

What you do, in order:

1. Finish Task 1 (create the design and connect its ports) and Task 2 (write data into all
   16 slots).
2. Run it and compare the waveform to the spec in the lesson.
3. Find and fix the bugs one at a time, rerunning after each fix.
4. Keep going until your waveform matches the golden version.

Try to do it without looking at `golden_counter_sram`. If you're stuck, use the hints in the
lesson, then look at the golden version before you ask an AI.

Build, run, and look, from inside your copy:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &
```

Exercise by Bryson Fields. Questions: the ASIC GroupMe, or email Bryson Fields
(bafields1@aggies.ncat.edu) or Zachary Johnson (zejohnson3@aggies.ncat.edu).
