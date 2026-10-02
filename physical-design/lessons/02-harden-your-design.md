# Lesson 2: Harden your design

**Goal:** run the LibreLane flow on the counter-SRAM you fixed in Block 2.

---

## Step 1: Get the latest version of the repo

```bash
cd ~/silicon-aggies-onboarding
git checkout main
git pull upstream main
```

Your Block 2 folder will look nearly empty on `main`. That's expected. Your work is on your
Block 2 branch, and Step 2 copies the one file you need out of it.

## Step 2: Set up your folder

Replace `YOUR-GITHUB-USERNAME` with your GitHub username:

```bash
mkdir -p submissions/physical-design/YOUR-GITHUB-USERNAME/src
cd submissions/physical-design/YOUR-GITHUB-USERNAME
cp ../../../physical-design/starter/config.yaml .
```

Now get your **fixed** counter-SRAM from Block 2. You saved it on your Block 2 branch, so
it isn't in the folder you're looking at right now. This command copies it straight out of
that branch. Replace `YOUR-GITHUB-USERNAME` with your username in both places. It's one
long line:

```bash
git show block2-YOUR-GITHUB-USERNAME:submissions/verification/YOUR-GITHUB-USERNAME/buggy_counter_sram/buggy_design/counter_sram.sv > src/counter_sram.sv
```

Check that it worked:

```bash
ls . src
head -20 src/counter_sram.sv
```

You should see `config.yaml` and `src`, and the start of your counter-SRAM code.

> **`fatal: invalid object name`?** The branch name is wrong. Run `git branch` to list your
> branches and use the one that starts with `block2`.
>
> **`fatal: path ... does not exist`?** The username in the path is wrong, or the file was
> saved somewhere else. Ask in the GroupMe. As a fallback, you can use the golden version:
> `cp ../../../verification/golden_counter_sram/counter_sram_design/counter_sram.sv src/`

Make sure you're hardening the fixed design. If you harden a broken one, you get a perfectly
manufacturable broken chip, and that really does happen to real companies.

## Step 3: Predict before you run

Open `src/counter_sram.sv` and count how many flip-flops the design needs. Every bit that a
`<=` inside `always_ff` has to remember becomes one flip-flop. Go through each register and
memory and add up its bits:

- the counter's `count`: how many bits?
- the SRAM's `memory`: how many slots, and how many bits in each?
- the SRAM's `read_data`: how many bits?

Write your total down. You'll check it against the tools' report in Lesson 3.

(The tutorial design used a real SRAM block that the factory provides, called a *macro*.
Our "SRAM" is just flip-flops. That's fine for 16 slots, but it gets big fast, which is why
real chips use macros for memory.)

## Step 4: Read the config

Open `config.yaml`. Every setting has a comment above it. The ones that matter most:

| Setting | What it means |
|---|---|
| `DESIGN_NAME` | The name of your top module. It must match the `module` line exactly: `counter_sram`. |
| `VERILOG_FILES` | Where your design file is. `dir::` means "starting from this config's folder." |
| `CLOCK_PERIOD` | How long one clock cycle is, in nanoseconds. 20 ns is 50 MHz: slow, so timing is easy to meet. |
| `FP_CORE_UTIL` | How much of the chip's core area gets filled with cells, in percent. Higher makes a smaller chip, but leaves less room for wires. |
| `PL_TARGET_DENSITY_PCT` | How tightly placement packs cells together. Usually a bit above `FP_CORE_UTIL`. |

The `PDN_...` lines at the bottom set up the power grid for a small chip. Leave them alone.

Don't change anything yet. Run it as-is first so you have a baseline to compare against.

## Step 5: Run the flow

Start the LibreLane environment if you're not already in it, then go back to your folder:

```bash
nix-shell ~/Su26LLEX/shell.nix
cd ~/silicon-aggies-onboarding/submissions/physical-design/YOUR-GITHUB-USERNAME
librelane config.yaml --run-tag first
```

The first time, LibreLane may download the sky130 PDK before it starts. That's a one-time
download.

Then it runs through every stage. Expect several minutes. When it finishes, the last lines
should say the flow completed. Your results are in `runs/first`.

If it stops with an error, look at the last 20 lines of output. The name of the step that
failed is there. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md), then post in the GroupMe
with those lines.

> **Running it again after a fix?** Add `--overwrite`:
> `librelane config.yaml --run-tag first --overwrite`. Without it, LibreLane quietly adds the
> new run on top of the old one in the same folder, and the commands in Lesson 3 end up
> reading both.

## Step 6: Find your results

```bash
ls runs/first
ls runs/first/final
```

Just like the tutorial, there's one numbered folder per step, and a `final` folder with the
results. The two things you'll use most:

- `runs/first/final/gds/counter_sram.gds`: your layout.
- `runs/first/final/metrics.csv`: a summary of every number the flow measured.

---

## Before you move on

- [ ] `src/counter_sram.sv` is your fixed design from Block 2.
- [ ] You wrote down how many flip-flops you expect.
- [ ] `librelane config.yaml --run-tag first` finished without errors.
- [ ] `runs/first/final/gds/counter_sram.gds` exists.

---

**Next:** [Lesson 3: Read the reports](03-read-the-reports.md).
