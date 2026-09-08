# Block 2 — Verification: Find the Bug

**Two-week rotation block. Oct 5 – Oct 16.**

Take something simple — an 8-bit counter — and write tests for it, including the weird
edge cases. Turn in the tests, the results, and a short write-up of what you found.

There is a twist. **The counter we give you is broken.** More than one thing is wrong
with it. The starter tests find one of them. The rest are yours to hunt down.

---

## Why this project

In industry, verification headcount runs roughly two to three engineers for every design
engineer, and most tapeout failures are verification failures rather than design
failures. Nobody tells you that in a digital logic class.

The concrete reason it matters to us: on Tiny Tapeout you get one shot. The chip comes
back in June 2027 and whatever you submitted in December is what you get. There is no
patch. A bug you did not test for is a bug that ships in silicon with your name on it.

You are also learning the exact harness the real submission uses. Tiny Tapeout's project
template tests with **cocotb driving Icarus Verilog**, which is what you are about to
use. The test file you write here is structurally the test file you submit in November.

---

## What you are testing

An 8-bit up-counter with load and enable.

```
ui_in[7:0]    load value
uio_in[0]     en    -- when high, count up by one each clock
uio_in[1]     load  -- when high, jump to the load value
uo_out[7:0]   the current count
rst_n         active low, synchronous
```

**The specification, which is the thing you test against:**

1. On reset, the count is 0.
2. When `en` is high and `load` is low, the count increases by one each clock.
3. When `en` is low and `load` is low, the count holds.
4. When `load` is high, the count becomes `ui_in`, **regardless of `en`.** Load wins.
5. Counting up from 255 wraps to 0.
6. Reset works at any time, in any state, whether or not `en` is high.

Read that list again. Each numbered line is at least one test.

---

## Step by step

### Step 1 — Set up

```bash
cd ~/silicon-aggies-onboarding
source .venv/bin/activate                        # every new terminal
mkdir -p submissions/verification/YOUR-GITHUB-USERNAME
cd submissions/verification/YOUR-GITHUB-USERNAME

cp ../../../verification/starter/Makefile .
cp ../../../verification/starter/test_counter.py .
cp ../../../verification/dut/tt_um_counter.v .
```

### Step 2 — Run the starter tests before you understand them

```bash
make
```

You should see four tests run, three pass, one fail. Read the failure message. It tells
you the value it wanted and the value it got.

Congratulations, you have found bug #1. There are more.

### Step 3 — Understand how a cocotb test works

Open `test_counter.py`. It is Python, not Verilog. Python drives the simulator: you set
input values, advance the clock, and read outputs back.

The four pieces you need:

```python
cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())   # start a clock
dut.rst_n.value = 0                                        # drive an input
await ClockCycles(dut.clk, 3)                              # advance time
assert int(dut.uo_out.value) == 0                          # check an output
```

That is genuinely most of it. Everything else is organization.

**The one trap that will cost you an hour if nobody warns you.** If you sample an output
at the exact instant of a clock edge, you read the *old* value — the flip-flops are
updating at that same moment. The starter file handles this with a helper:

```python
async def step(dut, n=1):
    await ClockCycles(dut.clk, n)
    await Timer(1, unit="ns")     # let everything settle before we look
```

Use `step()` everywhere instead of `ClockCycles` directly. If your test fails by exactly
one clock cycle, this is why.

### Step 4 — Write a test for every line of the spec

The starter covers spec lines 1, 2, 3, and 5. **Lines 4 and 6 have no test at all.** That
is not an accident.

Write them. Each test looks like this:

```python
@cocotb.test()
async def test_load_beats_enable(dut):
    """Spec line 4: when load and en are both high, load wins."""
    await setup(dut)
    set_ctrl(dut, en=1)
    await step(dut, 5)                  # get the counter somewhere non-zero

    dut.ui_in.value = 0x42
    set_ctrl(dut, en=1, load=1)         # BOTH high at once
    await step(dut)

    assert count(dut) == 0x42, f"load should win over en, got {count(dut)}"
```

Then keep going. Cases worth writing, roughly in order of how much they are worth:

- Load and enable asserted together (spec line 4).
- Reset asserted while `en` is low (spec line 6).
- Reset asserted mid-count, in the middle of counting up.
- Load a value, then immediately count from it.
- Load 255, then increment once.
- Load 0, load 255, load 0 back to back on consecutive cycles.
- Hold for 20 cycles and confirm the value never moves.
- Two resets back to back.

### Step 5 — Add a self-checking random test

Directed tests only find bugs you already thought of. A random test with a reference
model finds the ones you did not.

The idea: keep a Python integer that models what the counter *should* be doing, drive
random inputs, and compare every cycle.

```python
import random

@cocotb.test()
async def test_random_against_model(dut):
    await setup(dut)
    model = 0
    for _ in range(500):
        en   = random.randint(0, 1)
        load = random.randint(0, 1)
        val  = random.randint(0, 255)

        dut.ui_in.value = val
        set_ctrl(dut, en=en, load=load)
        await step(dut)

        # TODO: update `model` using the SPEC, not using the Verilog.
        #       Get this wrong and you will "prove" the broken counter is fine.

        assert count(dut) == model, f"mismatch: dut={count(dut)} model={model}"
```

Write the model from the spec text, not by reading the DUT. If you copy the DUT's logic
into your model you have written a test that agrees with the bug.

This is a scoreboard, in miniature. It is how real verification environments work.

### Step 6 — Fix the counter

Once your tests fail for the right reasons, fix `tt_um_counter.v` until everything passes.

Keep the broken version. Save it as `tt_um_counter_broken.v` so your write-up can point
at the specific lines.

**Do not "fix" the counter by weakening a test.** If that thought crosses your mind,
write it down and put it in the write-up — it is a more interesting observation than
most of what people turn in.

Your fixed counter is what you carry into Block 3 and harden into a layout, so make it
one you trust.

### Step 7 — Report what you found

`WRITEUP.md`, 300–500 words. Structure it like a real bug report:

For each bug:
- **What the symptom was.** Which test failed and what it printed.
- **What the root cause was.** Point at the line of Verilog.
- **What the fix was.**
- **Why the other tests missed it.** This is the interesting part. Every bug that hides
  from a test suite hides for a reason.

Then answer: which spec line was hardest to test, and how confident are you that the
counter is now correct? "Very confident" needs an argument behind it.

### Step 8 — Open the pull request

```bash
cd ~/silicon-aggies-onboarding
git checkout -b block2-yourname
git add submissions/verification/YOUR-GITHUB-USERNAME
git commit -m "Block 2: counter verification"
git push -u origin block2-yourname
```

---

## Deliverables

In `submissions/verification/YOUR-GITHUB-USERNAME/`:

- [ ] `test_counter.py` — starter tests plus **at least four** of your own
- [ ] `tt_um_counter.v` — the fixed counter
- [ ] `tt_um_counter_broken.v` — the original, kept for reference
- [ ] `results.txt` — paste of your final `make` output, all tests passing
- [ ] `WRITEUP.md` — the bug report
- [ ] PR opened by **Friday Oct 16, 11:59 PM**

## Definition of done

- `make` runs clean on the fixed counter, zero failures.
- Every one of the six spec lines has at least one test that would actually catch a
  violation of it.
- Your tests fail when run against `tt_um_counter_broken.v`. Check this — run
  `make DUT=tt_um_counter_broken.v` and confirm it fails. A test suite that passes on
  the broken design is not a test suite.
- The write-up names root causes, not just symptoms.

---

## Common problems

| Symptom | What is usually wrong |
|---|---|
| `cocotb: command not found` / `ModuleNotFoundError` | The venv is not active. `source .venv/bin/activate` |
| Everything fails by exactly one clock cycle | You used `ClockCycles` instead of `step()`. See Step 3 |
| `ValueError: Cannot convert ... to integer` | Signal is `x` or `z`. Something is undriven — usually you never released reset |
| `make` says no rule to make target | You are not in your submission folder, or the Makefile did not get copied |
| Tests pass but you know the design is broken | Your assertions are not actually asserting. Break the DUT on purpose and confirm your test notices |
| Test hangs forever | You are `await`ing something that never happens. Check that the clock is started |
| `TOPLEVEL` mismatch error | The module name in the .v file must match `TOPLEVEL` in the Makefile |

## If you finish early

1. Add coverage tracking — record which `(en, load)` combinations you actually exercised
   and print a summary. You will probably find you never hit one of the four.
2. Write a test that runs the counter through all 256 values and confirms every one
   appears exactly once.
3. Read Tiny Tapeout's template test file and identify what it does that yours does not.
