# Golden counter-SRAM (Lesson 3)

A working counter connected to a 16-slot memory (an SRAM), and a testbench that writes a
value into every slot and reads them all back.

**Instructions:** [Lesson 3: Run the golden counter-SRAM](../lessons/03-golden-counter-sram.md)

| File | What it is |
|---|---|
| `counter_sram_design/counter_sram.sv` | three modules: `counter`, `SRAM`, and `counter_sram`, which connects them |
| `testbench/counter_sram_tb.sv` | the testbench: resets, writes 0 to 15 into slots 0 to 15, then reads them back |

How the design fits together:

- The counter's output is the SRAM's address. Each clock, the counter moves the memory to
  the next slot.
- When `write_en` is 1, `write_data` is stored in the current slot on the rising edge.
- On every rising edge, `read_data` shows what's in the current slot. Because the read also
  happens on a clock edge, `read_data` appears one clock after the address.
- Reset sends the address back to 0.

Build, run, and look, from inside this folder:

```bash
verilator --binary --timing --trace --top-module test counter_sram_design/counter_sram.sv testbench/counter_sram_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &
```

Exercise by Bryson Fields. Questions: the ASIC GroupMe, or email Bryson Fields
(bafields1@aggies.ncat.edu) or Zachary Johnson (zejohnson3@aggies.ncat.edu).
