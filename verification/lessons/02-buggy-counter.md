# Lesson 2: Find the bugs in the counter

**Goal:** finish a testbench for a counter that has bugs in it, use the waveform to find the
bugs, and fix them.

This counter has **two bugs**. Try to find them from the waveform, not by staring at the
design. Finding bugs from a waveform is the skill this block is about. If you get stuck,
there are hints at the end of Step 6. Look at the golden version only after you've tried the
hints, and try those before you ask an AI.

---

## Step 1: Copy the buggy exercises into your submission folder

You'll work on copies, so the originals stay untouched for the "prove it" step at the end.
This copies both buggy exercises at once; you'll use the second one in Lesson 4.

```bash
cd ~/silicon-aggies-onboarding
mkdir -p submissions/verification/YOUR-GITHUB-USERNAME
cp -r verification/buggy_counter verification/buggy_counter_sram submissions/verification/YOUR-GITHUB-USERNAME/
cd submissions/verification/YOUR-GITHUB-USERNAME/buggy_counter
ls
```

You should see `README.md`, `buggy_design`, and `testbench`.

If you close your terminal and come back later, get back here with:

```bash
cd ~/silicon-aggies-onboarding/submissions/verification/YOUR-GITHUB-USERNAME/buggy_counter
```

## Step 2: Know what you're testing against

This is the same spec as Lesson 1. The counter is supposed to do exactly this:

1. When `rst_n` is 0 on a rising clock edge, `count` becomes 0.
2. When `rst_n` is 1 and `en` is 1, `count` goes up by one on every rising edge.
3. When `en` is 0, `count` stays the same.
4. Counting up from 15 goes back to 0.

The ports are the same as the golden counter too: `clk`, `rst_n`, `en`, and a 4-bit
`count`.

## Step 3: Fill in Parts 1 and 2 of the testbench

Open `testbench/counter_tb.sv`. It has the five parts from Lesson 0. Part 3 (the clock) and
Part 5 (`$finish`) are done. You fill in the rest.

**Part 1:** under the first TODO, declare the four signals. Each is one line, like
`logic clk;`. Remember that `count` is 4 bits wide.

**Part 2:** under the second TODO, create the counter and connect all four ports. Look back
at "Part 2: the DUT" in [Lesson 0](00-testbench-primer.md) if you don't remember the
format.

**Checkpoint.** Save the file, then build and run it even though there are no test steps
yet:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
```

If it prints `Verilog $finish`, your signals and connections are right. If it prints an
`%Error`, read the first one and fix it. The most common mistakes are a missing semicolon
after a `logic` line, a comma after the last port connection, or a missing comma between
two port connections. [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) has more.

## Step 4: Write the test steps

Now fill in steps A to D inside the `initial begin` block, one at a time. After each step,
rebuild, rerun, and look at the waveform. Building up in small pieces means that when
something breaks, you know it was the last thing you added.

Use the commands from the table in Lesson 0: set an input with `=`, and wait with
`@(posedge clk)`, `@(negedge clk)`, or `repeat (N) @(posedge clk)`.

**Step A: hold reset for two clock edges.** Here's the code for this one, as an example of
what the others look like:

```systemverilog
		// step A: hold reset for two clock edges
		rst_n = 0;
		en = 0;
		repeat (2) @(posedge clk);
```

**Step B: release reset, turn on `en`, and count for 20 edges.** Wait for a falling edge,
then set `rst_n` to 1 and `en` to 1, then wait for 20 rising edges. Twenty is more than 16,
so you'll see whether the count goes back to 0 after 15. (Spec lines 2 and 4.)

**Step C: turn `en` off for 4 edges.** Wait for a falling edge, set `en` to 0, then wait for
4 rising edges. (Spec line 3.)

**Step D: count a bit more, then reset in the middle of counting.** Wait for a falling
edge, set `en` to 1, and wait for 3 rising edges. Then wait for a falling edge, set `rst_n`
to 0, and wait for 2 rising edges. (Spec line 1, while the counter is busy.)

After each step, run all three commands:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
gtkwave dump.vcd &
```

If GTKWave is already open, you don't need to open it again. Press Ctrl+Shift+R in GTKWave
to reload the new waveform.

## Step 5: Compare the waveform to the spec

Add `clk`, `rst_n`, `en`, and `count` to the waveform (click `test`, select the signals,
click Append, then Shift+Alt+F). Set `count` to decimal: right-click it, choose
**Data Format**, then **Decimal**.

Here's what a **correct** counter would do with your test steps:

| Step | What `count` should do |
|---|---|
| A. hold reset | 0 |
| B. count for 20 edges | 1, 2, 3 ... 15, 0, 1, 2, 3, 4 |
| C. `en` off | stays at 4 |
| D. count, then reset | 5, 6, 7, then 0 |

Go through your waveform one step at a time. Wherever it doesn't match the table, write
down what you see. Be specific. "`count` jumps to 5 when `rst_n` goes to 1 and never
moves" is useful. "The counter is broken" isn't.

Keep these notes. They become the "symptom" part of your write-up in Lesson 5.

> **Is it my testbench or the design?** When the waveform looks wrong, check your testbench
> first. Look at `rst_n` and `en` in the waveform. Are they doing what you meant them to do
> at each step? If the inputs look right and `count` still looks wrong, the problem is in
> the design.

## Step 6: Find the bugs

Open `buggy_design/counter.sv`. For each symptom you wrote down, ask: which line of the
design decides what `count` does in that situation? Then compare that line to the spec.

There are two bugs. Both are small, only a few characters each.

<details>
<summary>Hint 1 (click to open)</summary>

Look at the exact moment in the waveform where `count` first goes wrong. What input changed
right before that?

</details>

<details>
<summary>Hint 2</summary>

`count` goes wrong right when `rst_n` changes. Which line of the design checks `rst_n`?
Is it checking for the right value? Remember that `rst_n` is active low.

</details>

<details>
<summary>Hint 3</summary>

Once the first bug is fixed, look at what `count` becomes during reset. The spec says it
should be 0. What value does the design set it to?

</details>

## Step 7: Fix them, one at a time

Fix one bug, then rebuild, rerun, and reload the waveform. Check that the symptom you
expected went away and nothing new broke. Then fix the next one.

Fixing one bug at a time is a good habit. If you change three things at once and something
new breaks, you won't know which change did it.

You're done when your waveform matches the "should do" table in Step 5 exactly, for every
step.

## Step 8: Take your screenshot

In GTKWave, show `clk`, `rst_n`, `en`, and `count` (in decimal), zoomed so the whole run
fits. Take a screenshot and save it as `waveform-counter.png` in your submission folder,
`submissions/verification/YOUR-GITHUB-USERNAME/`. That's one folder up from
`buggy_counter`.

> **Saving from Windows:** press Windows+Shift+S to take the screenshot. To find your
> Ubuntu folders in File Explorer, click **Linux** in the left sidebar, then **Ubuntu-24.04**,
> **home**, your username, and **silicon-aggies-onboarding**.

## Step 9: Prove your testbench catches the bugs

A testbench is only useful if it would have caught the bugs. Run your **finished**
testbench against the **original** buggy design, the one in `verification/` that you never
touched:

```bash
verilator --binary --timing --trace --top-module test ../../../../verification/buggy_counter/buggy_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
```

Reload the waveform. It should look wrong again, with both bugs visible. If one of the bugs
doesn't show up, your testbench is missing a case. Add it, and do this step again.

(`../../../../` means "go up four folders," from `buggy_counter` back to the top of the
repo.)

When you're done, rebuild with your fixed design so your folder is back to normal:

```bash
verilator --binary --timing --trace --top-module test buggy_design/counter.sv testbench/counter_tb.sv
```

---

## If you finish early

1. **Make the testbench check itself.** Right now *you* are the checker, reading the
   waveform. Add these two lines at the end of step B, right after its `repeat (20)` line:

   ```systemverilog
		#1;
		if (count !== 4'd4) $display("ERROR: after step B, count should be 4 but it is %0d", count);
   ```

   The `#1` waits 1 ns so the flip-flops have finished updating before you look. (If you
   check at the exact instant of the clock edge, you can read the old value.) Rebuild and
   run. With your fixed design it prints nothing extra. Against the original buggy design,
   it prints the error. Add a check like this at the end of every step. Real verification
   teams write testbenches this way so nobody has to read the waveform by eye.
2. **Count every value.** Write a loop that runs the counter through 32 edges and checks
   that every value from 0 to 15 shows up exactly twice.

---

## Before you move on

- [ ] Your testbench builds, runs, and shows every spec line in the waveform.
- [ ] Your fixed counter matches the "should do" table exactly.
- [ ] `waveform-counter.png` is saved in your submission folder.
- [ ] Your testbench shows both bugs when run against the original buggy design.
- [ ] You wrote down each symptom and the line that caused it.

---

**Next:** [Lesson 3: Run the golden counter-SRAM](03-golden-counter-sram.md).
