# Lesson 4: Find the bugs in the counter-SRAM

**Goal:** finish a half-written testbench, use it to find three bugs in the counter-SRAM,
and fix them.

This is the design you'll turn into a chip layout in Block 3, so make sure it's right.

---

## Step 1: Go to your copy

You already copied this exercise in Lesson 2, Step 1:

```bash
cd ~/silicon-aggies-onboarding/submissions/verification/YOUR-GITHUB-USERNAME/buggy_counter_sram
ls
```

You should see `README.md`, `buggy_design`, and `testbench`. If the folder isn't there, go
back to Lesson 2, Step 1 and run the `cp` command.

## Step 2: Finish the testbench, Task 1

Open `testbench/buggy_cosram_tb.sv`. Most of it is written. It has the signals, the clock,
the starting values, and the reset. Two parts are missing, marked `EXERCISE TASK #1` and
`EXERCISE TASK #2`.

**Task 1:** create the `counter_sram` design and connect all seven of its ports. It's the
same pattern as the counter in Lesson 2, just with more ports. The port names are in the
`counter_sram` module at the bottom of `buggy_design/counter_sram.sv`, and the testbench
signals already have the same names.

Remember: commas between connections, no comma after the last one, and a semicolon after
the closing `)`.

**Checkpoint.** Build and run:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
./obj_dir/Vtest
```

You should see `Verilog $finish`. If you get `%Error`, read the first one and fix it before
you go on.

## Step 3: Finish the testbench, Task 2

**Task 2:** write the data into all 16 memory boxes. Right now the testbench turns on
`write_en` and then immediately turns it off again, so nothing gets written.

Under the Task 2 comment, write a `for` loop that runs 16 times. Each time through the loop:

1. set `write_data` to the loop number,
2. wait for a rising edge (this is when the write happens), and
3. wait for a falling edge (so the next change is away from the rising edge).

Look back at Lesson 0 for the `for` loop format, and at Lesson 3, Step 4 for how to fit the
32-bit loop number into the 8-bit `write_data`.

> **Heads up:** if you write `write_data = i;` instead of `write_data = i[7:0];`, the build
> fails with `%Warning-WIDTHTRUNC` and `Exiting due to 1 warning(s)`. Verilator treats size
> mismatches as errors. That's on purpose. It catches real bugs.

**Checkpoint.** Build, run, and open the waveform:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &    # Ubuntu / Windows
surfer dump.vcd &     # Mac
```

Add the same seven signals as Lesson 3, with `write_data`, `address`, and `read_data` in
decimal.

Before you go on, check your testbench, not the design. Look at the inputs only: `write_en`
should be 1 for 16 clocks and then 0, and `write_data` should go 0, 1, 2 ... 15 during those
16 clocks. If the inputs aren't doing that, fix the testbench first.

## Step 4: Compare to the spec and write down every symptom

Here's the spec from Lesson 3:

1. `address` is the counter's count, and follows all four counter spec lines.
2. On a rising edge with `write_en` = 1, `write_data` is stored at the current `address`.
3. On a rising edge with `write_en` = 0, the memory doesn't change.
4. On every rising edge, `read_data` updates to the value stored at the current `address`,
   so it shows up one clock after the address.
5. When `rst_n` goes to 0, `address` goes back to 0.

And here's what the golden design did with this same testbench:

| Phase | `write_en` | `address` | `read_data` |
|---|---|---|---|
| reset | 0 | 0 | 0 |
| write | 1 | 0, 1, 2 ... 15 | 0 |
| read | 0 | 0, 1, 2 ... 15, then 0 again at the very end | 0, 0, 1, 2 ... 14, 15, one clock behind `address` |

(Lesson 3, Step 6 explains why the read phase starts at address 0 and why `read_data` starts
with two 0s.)

Compare your waveform against the table and write down everything that's different.

This design has **three bugs**. They hide behind each other: until the first one is fixed,
you can't see the second. So you may only see one clear symptom right now. That's normal.

## Step 5: Find, fix, rerun, repeat

Work in a loop:

1. Pick the most obvious symptom.
2. Decide which spec line it breaks.
3. Find the line in `buggy_design/counter_sram.sv` that controls that behavior. Compare it
   to the spec.
4. Fix that one line.
5. Rebuild, rerun, reload the waveform. Did the symptom go away? Did a new one appear?
6. Write down the symptom, the line, and the fix. Then go back to 1.

Stop when your waveform matches the golden table exactly.

<details>
<summary>Hint for bug 1</summary>

`address` never moves from 0. The address comes from the counter. Look at the `counter`
module at the top of the file. When is it supposed to count, and when does it actually
count?

</details>

<details>
<summary>Hint for bug 2</summary>

Once the address moves, `read_data` stays at 0 in the read phase, so the data never got
stored. Look at the `SRAM` module. When is it supposed to write, and when does it actually
write?

</details>

<details>
<summary>Hint for bug 3</summary>

Once the data shows up, look at the timing. In the golden design, `read_data` was one clock
*behind* `address`. Is it still? If `read_data` lines up with `address` instead, something is
changing on the wrong edge of the clock. Lesson 3, Step 8 had you try exactly this.

One warning while you're at this stage: the testbench changes `write_data` on the falling
edge. If the memory is also acting on the falling edge, the two happen at the same instant,
and which one goes first is up to the simulator. So don't trust the *values* you see in
`read_data` until this bug is fixed. Trust the timing.

</details>

## Step 6: Take your screenshot

Show all seven signals, with the three buses in decimal, zoomed so the whole run fits.
Save the screenshot as `waveform-counter-sram.png` in your submission folder
(`submissions/verification/YOUR-GITHUB-USERNAME/`, one folder up from `buggy_counter_sram`).
On a Mac, run `mv ~/Desktop/Screenshot*.png ../waveform-counter-sram.png` from
`buggy_counter_sram`.

## Step 7: Prove your testbench catches the bugs

Same idea as Lesson 2. Run your finished testbench against the original buggy design:

```bash
verilator --binary --timing --trace --top-module test ../../../../verification/buggy_counter_sram/buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
./obj_dir/Vtest
```

Reload the waveform. It should look wrong again. Then rebuild with your fixed design:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
```

## Step 8: Double-check against the golden design

Now that you're done, you can compare your fixed file with the golden one. From your
`buggy_counter_sram` folder:

```bash
diff buggy_design/counter_sram.sv ../../../../verification/golden_counter_sram/counter_sram_design/counter_sram.sv
```

`diff` prints the lines that are different between two files. If it prints nothing, your
fixed design matches the golden one. If it prints lines, look at each one. A different
comment or spacing is fine. A different line of logic means one of your fixes doesn't
match; check it against the spec.

---

## If you finish early

1. **Add a reset in the middle.** The testbench only resets at the start, so spec line 5
   gets tested only once. Add a reset partway through the read phase and check that
   `address` goes back to 0.
2. **Use a better data pattern.** Change your Task 2 loop to write `8'd100 + i[7:0]` instead
   of `i[7:0]`. Now the data and the address are different numbers, so a mix-up between them
   can't hide.
3. **Make it check itself.** Like the stretch goal in Lesson 2: during the read phase, add
   `$display("ERROR ...")` lines that fire when `read_data` isn't what you wrote.

---

## Before you move on

- [ ] Tasks 1 and 2 are done, and the testbench builds and runs.
- [ ] Your fixed design matches the golden table exactly.
- [ ] `waveform-counter-sram.png` is saved in your submission folder.
- [ ] Your testbench shows the bugs when run against the original buggy design.
- [ ] You wrote down all three symptoms, the line that caused each, and your fix.

---

**Next:** [Lesson 5: Turn in your work](05-submit.md).
