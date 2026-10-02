# Lesson 1: Run the golden counter

**Goal:** run a working counter and its testbench, and learn the three commands you'll use
for the rest of the block. You don't write any code in this lesson.

"Golden" means this version is known to be correct. You'll compare the buggy version
against it in Lesson 2.

---

## Step 1: Get the latest version of the repo

The Block 2 files may have been updated since you forked the repo. Pull in the latest:

```bash
cd ~/silicon-aggies-onboarding
git checkout main
git pull upstream main
```

`git checkout main` switches you off your Block 1 branch and back to the main copy. Your
Block 1 work is safe on its branch. `git pull upstream main` downloads anything new from
the main ASIC repo.

Two things that look wrong but aren't:

- If your Block 1 pull request hasn't been merged yet, your Block 1 folder now looks almost
  empty, with only a few `.vcd` and `.out` files left. Your real files are saved on your
  Block 1 branch, not on `main`. They come back whenever you
  `git checkout block1-YOUR-GITHUB-USERNAME`. (If it has been merged, your files are on
  `main` too, and the folder looks normal.)
- `git status` may say `Your branch is ahead of 'origin/main'`. That only means your
  computer has newer files from the ASIC repo than your fork on GitHub does. Leave it. You
  never push `main`.

If `git pull` says `fatal: 'upstream' does not appear to be a git repository`, you skipped
the last part of setup step A6. Run this, then try again:

```bash
git remote add upstream https://github.com/zjohnson2005/silicon-aggies-onboarding.git
```

## Step 2: Look around

```bash
cd ~/silicon-aggies-onboarding/verification/golden_counter
ls
```

You should see `README.md` and two folders: `counter_design` and `testbench`.

```
golden_counter/
├── counter_design/
│   └── counter.sv       the design (the DUT)
└── testbench/
    └── counter_tb.sv    the testbench that tests it
```

You run the golden exercises right here in the `verification/` folder. The files they
create are ignored by git, so you won't accidentally turn them in.

## Step 3: Read the design

Open `counter_design/counter.sv` in your editor (or run `nano counter_design/counter.sv`,
and press Ctrl+X to quit):

```systemverilog
module counter (
    input logic clk,
    input logic rst_n,
    input logic en,
    output logic [3:0] count
);

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            count <= 4'd0;
        end
        else if (en) begin
            count <= count + 1'b1;
        end
    end

endmodule
```

Four ports: a clock, an active-low reset, an enable, and a 4-bit count. On each rising edge:
if reset is on (`rst_n` is 0), count goes to 0. Otherwise, if `en` is 1, count goes up by
one. If neither is true, nothing happens, so count holds its value.

Count is 4 bits, so it can hold 0 to 15. What happens after 15? The same thing as the
blinker in Block 1: it rolls over to 0.

## Step 4: Read the testbench

Open `testbench/counter_tb.sv`. It has the same five parts from Lesson 0. Find each one:

1. **Signals:** four `logic` lines, one per port.
2. **The DUT:** `counter dut( ... );`
3. **The clock:** `always #10 clk = ~clk;`
4. **The test steps:** the big `initial begin` block. It has four numbered steps in the
   comments.
5. **The end:** `$finish;`

Read the four numbered steps in the comments. Before you run anything, write down what you
think `count` will do during each one.

## Step 5: Build and run it

Every simulation in this block takes the same three commands. Run them one at a time from
inside `golden_counter/`.

**Command 1: build.**

```bash
verilator --binary --timing --trace --top-module test counter_design/counter.sv testbench/counter_tb.sv
```

That's one long line. Paste it all at once. Here's what each piece does:

| Piece | Meaning |
|---|---|
| `verilator` | the tool |
| `--binary` | build a program you can run |
| `--timing` | allow delays like `#10` and `@(posedge clk)` in the testbench |
| `--trace` | allow the program to record a waveform |
| `--top-module test` | the outermost module is the one called `test` (the testbench) |
| `counter_design/counter.sv testbench/counter_tb.sv` | the files to build: the design and the testbench |

It prints a lot of lines about compiling. That's normal. It's done when the last line looks
like:

```
make: Leaving directory '.../golden_counter/obj_dir'
```

It created a folder called `obj_dir` that holds the program.

**Command 2: run.**

```bash
./obj_dir/Vtest
```

This runs the program Verilator built. You should see one line:

```
- testbench/counter_tb.sv:61: Verilog $finish
```

That means the simulation reached `$finish` on line 61 of the testbench. It also wrote a
waveform file called `dump.vcd`.

**Command 3: look.**

```bash
gtkwave dump.vcd &
```

> **On a Mac,** type `surfer` instead of `gtkwave`, here and in every later lesson:
> `surfer dump.vcd &`. Pick `test` in the panel on the left and click signal names to add
> them. To reload after a rerun, use Surfer's reload option instead of Ctrl+Shift+R.

> **The rule for this whole block:** if you change *any* `.sv` file, run all three
> commands again, starting with `verilator`. `./obj_dir/Vtest` keeps running the old program
> until you rebuild it.

## Step 6: Read the waveform

In GTKWave:

1. In the top-left panel, click **`test`**.
2. In the panel below, you'll see `clk`, `count[3:0]`, `en`, and `rst_n`. Select all four
   (click the first, then Shift+click the last).
3. Click **Append**.
4. Press **Shift+Alt+F** to zoom to fit.
5. GTKWave shows `count` in hexadecimal, so 10 through 15 appear as A through F. To see
   normal numbers, right-click `count[3:0]` in the signal list, then choose
   **Data Format**, then **Decimal**.

Now compare the waveform to what you wrote down in Step 4. You should see this, from left
to right:

| Testbench step | What you see |
|---|---|
| 1. hold reset | `rst_n` is 0, `count` is 0 |
| 2. count for 20 edges | `count` goes 1, 2, 3 ... 15, then 0, 1, 2, 3, 4 |
| 3. turn `en` off | `count` stays at 4 for four clock edges |
| 4. count, then reset | `count` goes 5, 6, 7, then back to 0 when `rst_n` drops |

Zoom in on a few clock edges (the magnifying glass with a plus sign). Notice that `count`
only ever changes right when `clk` rises, and the testbench only ever changes `en` and
`rst_n` when `clk` falls. That's the falling-edge habit from Lesson 0.

## Step 7: Match the waveform to the spec

Here's the counter spec from Lesson 0. For each line, find the spot in your waveform where
it happens:

| Spec line | Where you can see it |
|---|---|
| 1. `rst_n` = 0 on a rising edge makes `count` 0 | the start, and again at the very end |
| 2. `en` = 1 makes `count` go up by one each edge | step 2 |
| 3. `en` = 0 makes `count` hold | step 3 |
| 4. 15 goes back to 0 | the middle of step 2 |

Every spec line shows up somewhere. That's what makes this a complete test. In Lesson 2
you'll write a testbench that does the same thing for the buggy counter.

## Step 8: Break it on purpose

Change something, predict the result, run it, and check. Try these one at a time, and put
each back the way it was before you try the next.

1. In the testbench, change `repeat (20)` to `repeat (40)`. What will `count` do? Rebuild,
   rerun, and reload the waveform (Ctrl+Shift+R in GTKWave).
2. In the design, change `count + 1'b1` to `count + 2'd2`. Write down what you expect
   `count` to show during step 2, then run all three commands and check.
3. In the design, change `4'd0` to `4'd9`. Which part of the waveform changes?

When you're done, get back the original files with:

```bash
git restore counter_design/counter.sv testbench/counter_tb.sv
```

---

## Try it in a second simulator (optional)

Icarus Verilog from Block 1 can run this too:

```bash
iverilog -g2012 -o sim.out counter_design/counter.sv testbench/counter_tb.sv
vvp sim.out
gtkwave dump.vcd &
```

You'll see the same waveform. Now open the testbench and change `initial rst_n = 0;` to
`initial rst_n = 1;`, so reset never happens. Run both simulators again.

In Verilator, `count` still starts at 0 and counts normally. In Icarus, `count` shows as
`x`, which means unknown, and it stays unknown until the reset at the very end. Verilator starts every signal at 0. Icarus starts them as
unknown, which is what a real chip does when it powers on. A testbench that forgets reset
can look fine in Verilator and still be wrong. That's why every testbench in this block
holds reset first.

Put the file back with `git restore testbench/counter_tb.sv` when you're done.

---

## Before you move on

- [ ] You ran all three commands and saw `Verilog $finish`.
- [ ] You opened the waveform and found all four spec lines in it.
- [ ] You changed something, rebuilt, and saw the waveform change.

---

**Next:** [Lesson 2: Find the bugs in the counter](02-buggy-counter.md).
