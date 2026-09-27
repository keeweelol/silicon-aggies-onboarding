# Lesson 5: Change one thing

**Goal:** change one setting, run the flow again, and see what it does to your numbers.

Running a tutorial shows you the tools work. Changing a setting and explaining what happened
shows you understand what the settings do. This lesson is the difference between the two.

---

## Step 1: Pick one experiment

Choose **one** of these:

**Option A: a faster clock.** In `config.yaml`, change `CLOCK_PERIOD: 20` to
`CLOCK_PERIOD: 5`. That's asking the chip to run four times faster (200 MHz instead of
50 MHz). Does timing still close? What happens to WNS?

**Option B: pack it tighter.** In `config.yaml`, change `FP_CORE_UTIL: 40` to
`FP_CORE_UTIL: 70`, and `PL_TARGET_DENSITY_PCT: 45` to `PL_TARGET_DENSITY_PCT: 75`. That
asks for a smaller chip with the cells packed closer together. What happens to the die area
and the wire length? Does routing still succeed?

Before you run it, write down what you think will happen. Which numbers will go up, which
will go down, and will the flow still pass?

## Step 2: Run it with a new name

Use a different run tag so your first run is kept for comparison:

```bash
librelane config.yaml --run-tag second
```

(Remember: you need to be inside `nix-shell ~/Su26LLEX/shell.nix`, in your submission
folder.)

If the flow fails this time, that's a result too, not a disaster. Note which step failed and
what the error said. That goes in your write-up. Then set the value partway back (for
example, `CLOCK_PERIOD: 10`, or `FP_CORE_UTIL: 55`) and try again with `--run-tag third`.

## Step 3: Fill in the second column

Add a column to `metrics.md` for the new run:

```markdown
| Metric | Run: first | Run: second |
|---|---|---|
```

Fill it in with the same commands as Lesson 3, but with `second` in place of `first` in each
path. For example:

```bash
grep -E "^(design__instance__count|design__die__area|timing__setup__ws|timing__setup__tns|route__wirelength|route__drc_errors|magic__drc_error__count|design__lvs_error__count)," runs/second/final/metrics.csv
```

Under the table, write one line saying which setting you changed and from what to what.

## Step 4: Compare

Look at the two columns side by side. Which numbers changed? Which stayed the same? Did it
match your prediction?

Keep your notes. You'll use them in the write-up.

## Step 5: Decide what to turn in

Your `config.yaml` should have the setting you changed, as long as that run passed all three
must-pass checks (0 DRC, 0 LVS, WNS zero or positive). If your changed run failed, set
`config.yaml` back to the last value that passed, and say so in the write-up.

---

## Before you move on

- [ ] You changed one setting and ran the flow again under a new run tag.
- [ ] `metrics.md` has a second column for the new run.
- [ ] You can say in a sentence or two what the change did.

---

**Next:** [Lesson 6: Turn in your work](06-submit.md).
