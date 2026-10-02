# The automatic submission check (for leads)

Every pull request that touches `submissions/` runs
[`check-submission.yml`](workflows/check-submission.yml), which runs
[`scripts/check_submission.py`](scripts/check_submission.py). Students see a green check or a
red X on the pull request within a few minutes. Clicking **Details**, then **Summary**, shows
the full list with what to fix.

A passing check means the submission is ready for your review. It doesn't replace the review:
it can't judge whether a write-up is thoughtful, whether a screenshot is readable, or whether
the student understood what they did. Those are still yours.

## What it checks

**Every pull request**

- It only changes files inside one `submissions/<block>/<username>/` folder.
- The folder name matches the author's GitHub username (capitals don't matter).

**Block 1 (digital design)**

- Runs the repo's own `check.py` and `tb_traffic_light.v` against the student's design, not
  the copies in their folder. A student who copied an older testbench is still held to the
  current one.
- The state diagram and waveform are real PNG or JPEG images (not HEIC, not empty files).

**Block 2 (verification)**

- All seven files are there, and both screenshots are real images.
- **Each testbench catches every planted bug, one at a time.** The check builds a copy of the
  design with only one bug in it, for each bug, and runs the student's testbench on it. If the
  waveform looks exactly like the golden design's, that bug went unnoticed.
- **Each testbench makes every spec line happen:** counting past 15, holding when `en` is 0,
  and a reset in the middle of counting; and for the counter-SRAM, writing and reading all 16
  slots.
- **Each fixed design behaves exactly like the golden one**, under the student's testbench,
  the golden testbench, and a testbench with a few hundred cycles of random inputs and resets
  ([`scripts/tb/`](scripts/tb)). A fix that only works for the lesson's inputs gets caught.
- No template text left in the write-up, and at least 250 words.

**Block 3 (physical design)**

- All seven files are there; screenshots are real images.
- `src/counter_sram.sv` behaves exactly like the golden design (same tests as Block 2).
- `config.yaml` names `counter_sram`, points at `src/counter_sram.sv`, and has a numeric clock
  period.
- `counter_sram.gds` is a real GDS file that contains a `counter_sram` cell (so it isn't the
  tutorial's layout, or a renamed text file).
- `metrics.md` has two runs, and at least one of them has 0 DRC, 0 LVS, and WNS zero or
  positive.
- All six stages are filled in in the write-up, with no template text left.

It does **not** run LibreLane. That would take most of an hour per pull request. The GDS and
metrics checks catch the common mistakes. Spot-check the numbers against the screenshots.

## Running it yourself

From the top of the repo, with Icarus Verilog and Verilator installed:

```bash
python3 .github/scripts/check_submission.py submissions/verification/SOME-USERNAME
```

Students can run it the same way before they push.

## Repo settings to change once

1. **Let the check run without approval.** By default GitHub won't run workflows on a pull
   request from someone who hasn't contributed before until a maintainer approves it, and for
   new members that's every first pull request. Go to **Settings > Actions > General > Approval
   for running fork pull request workflows from contributors**, and choose
   **Require approval for first-time contributors who are new to GitHub**.
2. **Leave it optional (not a required status check).** The workflow only runs on pull
   requests that touch `submissions/`. If you made it required in branch protection, your own
   pull requests that only change lessons would wait forever for a check that never starts.
   A red X is easy enough to see without blocking the merge button.

## Two things to know

- **A pull request that changes `.github/` can change its own check.** For `pull_request`
  events, GitHub runs the workflow file from the pull request itself. The check flags any
  change outside the submission folder, but a student who also edited the check could make it
  pass anyway. If a submission pull request touches `.github/`, don't trust its green check.
- **Don't switch the trigger to `pull_request_target`** to get comments posted on the pull
  request. That gives code students wrote access to the repo's secrets and a write token. The
  summary page already shows students everything; comments can be added later, safely, with a
  second workflow triggered by `workflow_run`.
