# Lesson 5: Turn in your work

About 45 minutes: most of it is the write-up. The git part is the same as Block 1.

---

## Step 1: Check that everything is there

```bash
cd ~/silicon-aggies-onboarding/submissions/verification/YOUR-GITHUB-USERNAME
ls
ls buggy_counter/testbench buggy_counter/buggy_design
ls buggy_counter_sram/testbench buggy_counter_sram/buggy_design
```

You should have:

- [ ] `buggy_counter/testbench/counter_tb.sv`: your testbench (Lesson 2)
- [ ] `buggy_counter/buggy_design/counter.sv`: your fixed counter (Lesson 2)
- [ ] `buggy_counter_sram/testbench/buggy_cosram_tb.sv`: Tasks 1 and 2 done (Lesson 4)
- [ ] `buggy_counter_sram/buggy_design/counter_sram.sv`: your fixed counter-SRAM (Lesson 4)
- [ ] `waveform-counter.png` (Lesson 2)
- [ ] `waveform-counter-sram.png` (Lesson 4)

The screenshots should be directly in your folder, next to `buggy_counter` and
`buggy_counter_sram`, not inside them.

## Step 2: Run both one last time

A lead will run exactly these commands on your files, so run them yourself first:

```bash
cd buggy_counter
verilator --binary --timing --trace --top-module test buggy_design/counter.sv testbench/counter_tb.sv
./obj_dir/Vtest
cd ../buggy_counter_sram
verilator --binary --timing --trace --top-module test buggy_design/counter_sram.sv testbench/buggy_cosram_tb.sv
./obj_dir/Vtest
cd ..
```

Both should end with `Verilog $finish` and no `%Error` lines.

## Step 3: Write the bug report

Copy the template into your folder:

```bash
cp ../../../verification/submission-template/WRITEUP.md .
```

Open `WRITEUP.md` and fill it in, 300 to 500 words. You found five bugs in total, two in the
counter and three in the counter-SRAM. For each one, the template asks for:

- **the symptom:** what you saw in the waveform. Use the notes you took.
- **the spec line it broke.**
- **the root cause:** the exact line of code, and why it was wrong.
- **the fix.**

A **root cause** is the actual line that's wrong, not what it looked like from the outside.
"`count` stuck at 5" is a symptom. "Line 12 checks `if (rst_n)` but reset is active low, so
it should be `if (!rst_n)`" is a root cause.

## Step 4: Branch, commit, and push

These are the same steps as Block 1. [SUBMITTING.md](../../SUBMITTING.md) explains each one.

```bash
cd ~/silicon-aggies-onboarding
git status
git checkout -b block2-YOUR-GITHUB-USERNAME
git add submissions/verification/YOUR-GITHUB-USERNAME
git status
```

The first `git status` should say `On branch main`. The second one lists what you're about
to turn in, under **Changes to be committed**. It should show only files in your folder,
and **no** `obj_dir` folders or `.vcd` files. If it does, stop and ask in the GroupMe.

```bash
git commit -m "Block 2: design verification"
git push -u origin block2-YOUR-GITHUB-USERNAME
```

## Step 5: Open the pull request

1. Go to your fork on GitHub and click **Compare & pull request**.
2. Check that it goes from your `block2-...` branch into `main` on
   `zjohnson2005/silicon-aggies-onboarding`.
3. Title it: `Block 2: Your Name (your-github-username)`
4. Fill in the form in the description. Drag **both** waveform screenshots into the
   Screenshots section, keep only the Block 2 checklist, and fill it in.
5. Click **Create pull request**.

If a lead asks for changes, see [how to respond](../../SUBMITTING.md#how-to-respond).

---

That's Block 2. Your fixed `counter_sram.sv` is the design you take into Block 3.

**Next:** [Block 3: Physical Design](../../physical-design/README.md).
