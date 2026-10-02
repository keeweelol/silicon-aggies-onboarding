# Lesson 3: Run the golden counter-SRAM

**Goal:** understand a slightly bigger design, a counter wired to a small memory, and read
its waveform. You don't write any code in this lesson.

---

## Step 1: What an SRAM is

An **SRAM** is a small memory. Picture a row of 16 numbered boxes. Each box holds one 8-bit
number (0 to 255).

- The box number is called the **address**. With 16 boxes, addresses go from 0 to 15, so an
  address fits in 4 bits.
- To **write**, you pick an address, put a number on `write_data`, and turn on `write_en`
  (write enable). On the next rising clock edge, the number goes into that box.
- To **read**, you pick an address. On the next rising clock edge, whatever is in that box
  shows up on `read_data`.

In this design, you don't pick the address yourself. The counter from Lessons 1 and 2 picks
it. Every clock edge the counter goes up by one, so the memory steps through boxes 0, 1, 2,
and so on, one per clock.

## Step 2: Look at the files

```bash
cd ~/silicon-aggies-onboarding/verification/golden_counter_sram
ls
```

```
golden_counter_sram/
├── counter_sram_design/
│   └── counter_sram.sv       three modules in one file
└── testbench/
    └── counter_sram_tb.sv
```

## Step 3: Read the design

Open `counter_sram_design/counter_sram.sv`. It has three modules.

**1. `counter`:** the same 4-bit counter you already know.

**2. `SRAM`:** the memory.

```systemverilog
logic [7:0] memory [0:15];      // 16 boxes, 8 bits each

always_ff @(posedge clk) begin
    if (write_en) begin
        memory[address] <= write_data;   // write, if write_en is on
    end
    read_data <= memory[address];        // read, every clock
end
```

`logic [7:0] memory [0:15];` reads as "16 things, numbered 0 to 15, each 8 bits wide."
`memory[address]` means "the box at this address."

**3. `counter_sram`:** the **top-level** module, the one that holds the other two and wires
them together. The line to look at is inside the counter instance:

```systemverilog
.count(address)
```

The counter's `count` output is connected to a wire called `address`, and that same wire
goes into the SRAM. That single connection is how the counter picks the memory address.

## Step 4: Read the testbench

Open `testbench/counter_sram_tb.sv`. Same five parts as before. The test steps do three
things:

1. Hold reset for two clock edges.
2. **Write phase:** turn on `en` and `write_en`, then use a `for` loop to put 0, 1, 2 ... 15
   on `write_data`, one per clock. Box 0 gets 0, box 1 gets 1, and so on.
3. **Read phase:** turn off `write_en` and wait 16 more clocks. The counter keeps going,
   so the memory reads every box back out.

Look at line 52: `write_data = i[7:0];`. The loop counter `i` is 32 bits, but `write_data`
is only 8. `i[7:0]` takes just the bottom 8 bits so the sizes match. Remember this. You'll
need it in Lesson 4.

## Step 5: Build, run, look

The same three commands as always, with this exercise's file names:

```bash
verilator --binary --timing --trace --top-module test counter_sram_design/counter_sram.sv testbench/counter_sram_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &
```

The run should print `Verilog $finish`.

In GTKWave, click `test` and add all seven signals: `clk`, `rst_n`, `en`, `write_en`,
`write_data`, `address`, and `read_data`. Set `write_data`, `address`, and `read_data` to
decimal (right-click, **Data Format**, **Decimal**). You can select all three and change
them at once. Then press Shift+Alt+F.

## Step 6: Read the waveform

Here's what you should see:

| Phase | `write_en` | `address` | `read_data` |
|---|---|---|---|
| reset | 0 | 0 | 0 |
| write | 1 | 0, 1, 2 ... 15 | 0 (nothing useful yet) |
| read | 0 | 0, 1, 2 ... 15, then 0 again at the very end | 0, 0, 1, 2 ... 14, 15 |

The read phase starts back at address 0, because by the end of the write phase the counter
has already rolled over from 15 to 0. And `read_data` starts with two 0s: the first is left
over from the write phase, and the second is box 0's value, arriving one clock after
`address` was 0.

Zoom in on the read phase and look closely at `address` and `read_data` together.
`read_data` is always **one clock behind** `address`. When the address changes to 5,
`read_data` shows what's in box 4.

That's because the read happens on a clock edge, just like the write. On each rising edge,
the SRAM grabs whatever is in the box at the *current* address, and at that same edge, the
counter moves on to the next address. So by the time you see the data, the address has
already moved forward by one. It isn't a bug. Plenty of real memories work this way.

## Step 7: The spec

This is what the counter-SRAM is supposed to do. You'll test the buggy version against it
in Lesson 4.

1. `address` is the counter's count, and follows all four counter spec lines from Lesson 2.
2. On a rising edge with `write_en` = 1, `write_data` is stored at the current `address`.
3. On a rising edge with `write_en` = 0, the memory doesn't change.
4. On every rising edge, `read_data` updates to the value stored at the current `address`,
   so it shows up one clock after the address.
5. When `rst_n` goes to 0, `address` goes back to 0.

Find each line in your waveform. (Spec line 5 is only at the very start in this testbench.)

## Step 8: Break it on purpose

Try these one at a time, rebuilding and reloading each time.

1. On line 52, change `write_data = i[7:0];` to `write_data = i[7:0] * 2;`. What will
   `read_data` show in the read phase? Predict first, then check.
2. Now change it to `write_data = 8'd100 + i[7:0];`. Predict, then check.
3. In the design, change `posedge` to `negedge` in the SRAM's `always_ff` line only. What
   changes about the one-clock delay between `address` and `read_data`? (Watch the timing,
   not the exact values. The testbench changes `write_data` on the falling edge too, so
   which one goes first at that instant is up to the simulator.)

Put everything back when you're done:

```bash
git restore counter_sram_design/counter_sram.sv testbench/counter_sram_tb.sv
```

## Think about it (optional)

The golden testbench writes the value `i` into box `i`: box 3 holds 3, box 7 holds 7. That
makes the waveform easy to read. It also hides a whole kind of bug. Suppose someone wired
the design so the data and the address got swapped. Would this testbench notice? Why is a
pattern like `8'd100 + i[7:0]` from Step 8 a better test?

---

## Before you move on

- [ ] You ran the golden counter-SRAM and saw `Verilog $finish`.
- [ ] You can point to the write phase and the read phase in the waveform.
- [ ] You can explain why `read_data` is one clock behind `address`.

---

**Next:** [Lesson 4: Find the bugs in the counter-SRAM](04-buggy-counter-sram.md).
