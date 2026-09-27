# Golden counter (Lesson 1)

A working 4-bit counter and a testbench that tests it. "Golden" means it's known to be
correct, so you can compare the buggy version against it later.

**Instructions:** [Lesson 1: Run the golden counter](../lessons/01-golden-counter.md)

| File | What it is |
|---|---|
| `counter_design/counter.sv` | the counter: clock, active-low reset, enable, and a 4-bit count |
| `testbench/counter_tb.sv` | the testbench: resets, counts past 15, pauses, and resets mid-count |

Build, run, and look, from inside this folder:

```bash
verilator --binary --timing --trace --top-module test counter_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &
```

Exercise by Bryson Fields. Questions: the ASIC GroupMe, or email Bryson Fields
(bafields1@aggies.ncat.edu) or Zachary Johnson (zejohnson3@aggies.ncat.edu).
