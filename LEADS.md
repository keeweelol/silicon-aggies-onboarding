# Teaching Runbook — Leads Only

How to actually run the six weeks. If you are a new member, this file is not for you,
though nothing in it is secret.

---

## 1. The teaching model

**We do not lecture.**

Each two-week block runs on the same three-part rhythm:

| When | What | Length | Who |
|---|---|---|---|
| Day 1 (Monday) | **Kickoff demo.** A lead runs the whole project live in front of the room and shows the finished result | 30 min | Block lead |
| Middle weekend | **Open lab.** Leads physically present, members work on their own machines | 2–3 hrs | All leads |
| Everything else | **Async.** `#help` channel, PR comments | — | Rotating |

The demo exists so members know what they are aiming at. The open lab exists because
some problems only get solved by someone looking at your screen. Everything else is
written material.

**This model only works if the written material is good enough to follow without a person
standing there.** That is why the block guides in this repo matter more than any single
meeting, and why they are frozen on September 12 rather than written as we go.

## 2. Roles

Three teaching leads for fall, one per block. Functional teams do not exist yet — they
start in spring with chipIgnite work. A teaching lead owns:

- Running their block's kickoff demo
- Being the primary `#help` responder during their two weeks
- Reviewing every PR for their block
- Keeping their block's guide accurate — if three people hit the same error, it goes in
  the Common Problems table before the block ends

Leads for the block that is *not* running still show up to open lab. Fifty members and
one lead does not work.

## 3. How to run a kickoff demo

Thirty minutes, and stick to it. The shape is the same every time:

1. **(3 min) Show the finished thing first.** The working waveform, the passing test
   suite, the layout in KLayout. People need a picture of the destination.
2. **(5 min) Say why this block exists.** One honest sentence about what it connects to.
   Not motivational — connective. "The tile you tape out in December has a controller
   in it that is the same shape as this."
3. **(15 min) Do it live, from an empty folder.** Type the commands. Let it fail if it
   fails, and fix it in front of them. Watching a lead recover from an error is worth
   more than watching a lead be smooth.
4. **(5 min) Walk the deliverables list and the deadline.** Literally read the checkboxes.
5. **(2 min) Say where to get help and what a good `#help` post looks like.**

**Do not** explain the theory first. Do not open slides. If you find yourself explaining
what a finite state machine is before showing one, you have lost the room.

## 4. Per-block notes

### Block 1 — Digital Design (Sep 21 – Oct 2)

**Demo:** write a two-state FSM from scratch, compile, run, open GTKWave, drag signals
in. The GTKWave part is the most valuable ninety seconds of the demo — most members have
never seen a waveform viewer and it is not obvious how to use one.

**Where they get stuck, in order of frequency:**

1. `iverilog` without `-g2012`, then a wall of syntax errors on valid code.
2. Blocking (`=`) vs nonblocking (`<=`) in a clocked block. Say this in the demo, then
   say it again.
3. Reading `ped_button` directly in the GREEN state instead of latching it. This is the
   actual pedagogical point of the project — a one-cycle event that has to be remembered.
   Do not give it away in the demo, but recognize it fast in PR review.
4. Not resetting the timer on every state transition, producing a light that flickers.
5. GTKWave on Windows 10 without an X server. Have the Surfer web viewer link ready.

**Reference solution:** `leads/solutions/tt_um_traffic_light_ref.v`. Do not put this in
the member-facing tree.

**Look for in review:** the state diagram photo (people skip it), whether the outputs are
driven from `state` rather than being separate registers, and whether the write-up
answers the "what broke" question honestly.

### Block 2 — Verification (Oct 5 – Oct 16)

**Demo:** run `make` on the broken counter live. Let the failure print. Then walk the
failure message word by word — which test, what it expected, what it got. Then open the
DUT and find the line. That whole loop in five minutes is the entire block in miniature.

**Where they get stuck:**

1. Forgetting `source .venv/bin/activate`. This will happen more than everything else
   combined. Put it in the demo twice.
2. The sampling race — reading an output at the clock edge and getting the old value.
   The `step()` helper in the starter handles it, but people who write their own
   `ClockCycles` calls will hit it and the symptom is "everything is off by one."
3. Writing a reference model by copying the DUT logic, which produces a test suite that
   agrees with the bug. Call this out explicitly in the demo — it is the deepest idea in
   the block.
4. "Fixing" the DUT by loosening an assertion.

**The planted bugs:** the shipped DUT has a saturating counter (no rollover at 255) and
inverted load/enable priority. The starter tests catch the first. The second is only
found by a test that asserts `load` and `en` together, which nothing in the starter does.
That is deliberate — do not hint at it, and note in review who found it and how.

**Reference:** `leads/solutions/tt_um_counter_correct.v`.

**Look for in review:** whether their tests actually fail against the broken version.
Make them prove it — `make DUT=tt_um_counter_broken.v` should be red. Several people will
turn in tests that pass on everything.

### Block 3 — Physical Design (Oct 19 – Oct 30)

**Demo:** the run takes too long to do live end to end. Start the run at the beginning of
the demo, talk over it, and have a completed run directory open in another window to
show the outputs. Then KLayout, with layers toggling.

**Where they get stuck:**

1. **Environment.** This block is 80% environment problems and 20% design. Sort machine
   access in September, not on October 19. Anyone who cannot run Nix locally needs a lab
   machine reservation before the block opens.
2. Non-synthesizable constructs left in RTL from Block 1 habits.
3. `DESIGN_NAME` not matching the module name.
4. Committing the run directory. Watch for PRs with thousands of files and reject them
   immediately with a pointer to the `.gitignore`.

**Pre-block dependency:** the Su26LLEX cleanup — nested directory note in the README,
typo fixes, pinned LibreLane version. Owner: Bryson. Due September 12. If the version is
not pinned, everyone's metrics will differ and the write-ups become uncomparable.

**Look for in review:** whether the metrics table is filled from their own run or copied
from a neighbor. Numbers should differ slightly between people once they do Step 7.

## 5. PR review

Review within 72 hours of the PR opening. A member sitting on an unreviewed PR for a week
learns that deadlines are one-directional, and you will not get that trust back.

**Merge when:** every deliverable is present, it runs, the write-up is in their own words.

**Request changes when:** something is missing or broken. Be specific and be short. "The
waveform screenshot does not show a pedestrian interrupt — can you add one?" is a good
review. A paragraph of encouragement wrapped around a vague concern is not.

**Never:** leave a review that only says "looks good" on work that does not. The rotation
is a placement mechanism and inflated reviews destroy it.

Keep a running spreadsheet: member, block, submitted on time (Y/N), quality note, which
team they seemed to enjoy. That spreadsheet is the input to placement week.

## 6. Stragglers

The completion bar is firm, but the failure mode we care about is the person who hits an
environment wall in week one, gets quiet, and never comes back.

- If someone has not posted in `#help` and has not opened a PR by the Wednesday of week
  two, a lead messages them directly. Not a group ping.
- Late is fine with notice. Silent and missing is what we chase.
- Missing one block does not end the rotation. Missing two does — talk to them about
  spring instead.

## 7. Placement week (Nov 2)

Members rank all three teams. Leads bring the spreadsheet. Where a member's preference
and the lead read match, it is automatic. Where they differ, the member's preference
wins — the rotation exists to inform their choice, not to override it.

If a team ends up badly under-subscribed even after rotation, that is information about
how we taught that block, not about the members.

## 8. Pre-semester checklist

Everything below is due **September 12**, one week before the interest meeting.

| Item | Owner | Status |
|---|---|---|
| Confirm rotation order (Digital → Verification → Physical) with Dr. Limbrick | Zach | |
| Su26LLEX cleanup: nested-dir note, typos, pin LibreLane version | Bryson | |
| Verify toolchain installs clean on Ubuntu, macOS, and WSL2 | | |
| Verify Block 1 flow end to end on a fresh machine | | |
| Verify Block 2 `make` runs on a fresh venv | | |
| Verify Block 3 completes on a lab machine and on a student laptop | | |
| Create GitHub org, push this repo, enable PR reviews | | |
| Reserve lab machines for members who cannot run LibreLane locally | | |
| Confirm room + time for three kickoff demos and three open labs | | |
| Set up `#help` channel with a pinned "how to ask" post | | |
| Recruit and brief the three teaching leads | | |

## 9. What to tell Dr. Limbrick

The short version of the program, if you have three minutes with him:

> Every new member does three two-week projects — one in each of digital design,
> verification, and physical design — before choosing a team. We rotate rather than let
> people self-select because Silicon Jackets found self-selection sends two thirds of
> members to digital design and starves the other two teams. All three projects use the
> Tiny Tapeout pin contract and the same tools as the December submission, so the
> rotation is direct preparation for the tapeout rather than a separate onboarding
> exercise. Everything is submitted as a pull request to the org GitHub, which gives us
> a reviewable record of who completed what, and gives every member public commits on a
> chip design project. The written guides are frozen a week before the interest meeting.
> What we need from you: confirmation on the rotation order, lab machine access for
> members who cannot run the toolchain locally, and a read on whether the completion bar
> is set where you would set it.
