# Teaching runbook (for leads)

How to run the six weeks. New members don't need this file, but nothing in it is secret.

---

## 1. Why the program is built this way

### Rotation instead of letting people pick

Every new member does all three blocks before choosing a team. Silicon Jackets at Georgia
Tech started out letting members join whichever subteam they liked, then switched to
requiring all three. When students choose based on what they already know, more than two
thirds pick digital design. That leaves verification and physical design short of people,
and it leaves members with no picture of how the whole flow fits together.

Rotation costs some depth inside each block. In exchange, members make a better-informed
choice and the teams end up more evenly staffed. We're taking that trade.

There's a practical reason too. When the whole cohort is on the same block at the same
time, a tooling problem that hits fifty people gets solved once. Rolling admission would
mean re-solving the same install problems all semester.

### What onboarding is filtering for

Effort and follow-through, not existing skill. The projects are meant to be doable by
someone who has taken digital logic and nothing else. A member who finishes three small
projects on time over six weeks will be useful. A member who doesn't, won't, however much
Verilog they knew coming in. Keep the technical bar low and the completion bar firm.

### Block order

Digital Design, then Verification, then Physical Design. That's the order the work happens
in industry: describe the hardware, prove it works, turn it into geometry. It also lets each
block feed the next. The counter-SRAM members debug in Block 2 is the design they harden in
Block 3, so nobody is handed a black box.

### How it connects to the tapeout

- Block 1 uses the Tiny Tapeout pin contract (`clk`, `rst_n`, `ena`, `ui_in`, `uo_out`,
  `uio_*`, and a `tt_um_` module name). By November nobody is learning the interface for
  the first time.
- Block 2 has members write their own SystemVerilog testbenches and trace a symptom in a
  waveform back to a line of RTL. Every tile needs that before it ships. The exercises are
  Bryson Fields's.
- Block 3 uses LibreLane on sky130, the same flow that hardens the tile.

By November 2, a member who finished the rotation has written a state machine, written a
testbench that found real bugs, and produced a GDS. The MAC tile is a harder version of
three things they've each done once.

---

## 2. The teaching model

We don't lecture. Each two-week block runs on the same rhythm:

| When | What | Length | Who |
|---|---|---|---|
| Monday, week 1 | **Kickoff demo.** A lead does the whole project live and shows the finished result | 30 min | Block lead |
| Middle weekend | **Open lab.** Leads in the room, members on their own laptops | 2 to 3 hrs | All leads |
| Everything else | Questions in the GroupMe, PR comments | ongoing | Rotating |

The demo shows members what they're aiming at. The open lab is for problems that only get
solved by someone looking at your screen. Everything else is the written guides.

This only works if the guides are good enough to follow with nobody standing there. That's
why the guides matter more than any single meeting. When three people hit the same error,
add it to that block's TROUBLESHOOTING.md before the block ends.

## 3. Roles

Three teaching leads this fall, one per block. Functional teams start in spring with
chipIgnite work. A teaching lead:

- runs their block's kickoff demo,
- is the main person answering GroupMe questions during their two weeks,
- reviews every PR for their block, and
- keeps their block's guides accurate.

Leads whose block isn't running still come to open lab. One lead can't cover fifty members.

## 4. How to run a kickoff demo

Thirty minutes. The shape is the same every time:

1. **Show the finished thing first (3 min).** The working waveform, the passing tests, the
   layout in KLayout. People need to see where they're headed.
2. **Say why the block exists (5 min).** One sentence about what it connects to, like "the
   tile you tape out has a controller in it that's the same shape as this."
3. **Do it live from an empty folder (15 min).** Type the commands. If something fails, fix
   it in front of them. Watching a lead recover from an error teaches more than watching a
   lead be smooth.
4. **Read the deliverables list and the deadline out loud (5 min).**
5. **Say where to get help and what a good question looks like (2 min).** Command, full
   error text, operating system.

Don't start with theory, and don't open slides. If you're explaining what a state machine
is before you've shown one, you've lost the room.

---

## 5. Block notes

### Block 1: Digital Design (Sep 21 to Oct 2)

**Demo:** write a two-state FSM from scratch, compile, run, open GTKWave, and drag signals
in. The GTKWave part is the most useful ninety seconds of the demo. Most members have never
seen a waveform viewer, and it isn't obvious how to use one.

**Where they get stuck, most common first:**

1. Running `iverilog` without `-g2012` and getting a wall of syntax errors on valid code.
   `make` handles this, so point them back to `make`.
2. Blocking (`=`) vs nonblocking (`<=`) in a clocked block. Say it in the demo, then say it
   again.
3. Reading `ped_button` directly in the GREEN state instead of latching it. This is the
   main lesson of the project: a one-cycle event has to be remembered. Don't give it away
   in the demo, but recognize it fast in review.
4. Not resetting the timer on every state change, which makes the light flicker.
5. GTKWave on Windows 10 without an X server. Have the Surfer link ready.

**Reference solution:** keep it outside this repo so members can't find it.

**In review, look at:** the state diagram photo (people skip it), whether the outputs come
from `state` instead of separate registers, and whether the write-up answers "what broke"
honestly.

### Block 2: Verification (Oct 5 to Oct 16)

The exercises are Bryson's. The originals are in `bdawgcodes28/Design-Verification-Exercises`.
If he changes one there, copy the change here before the block opens so the two don't drift
apart.

This copy differs from his in a few places, all to make it easier for beginners:

- The golden counter testbench holds reset before counting. His doesn't (see stuck point 5).
- Exercise 2 ships with a testbench outline full of TODOs instead of an empty folder.
- The lessons tell members how many bugs each design has.
- Exercise 4 has members finish the testbench before touching the design, so they find the
  bugs from the waveform instead of by reading code.
- His per-exercise instructions now live in `verification/lessons/`, and each exercise
  folder's README points there.

**Demo:** run the golden counter live with the three-command loop (`verilator`,
`./obj_dir/Vtest`, `gtkwave dump.vcd`), add signals in GTKWave, and point out what each spec
line looks like on screen. Then compile the *buggy* counter against the same testbench and
show the two waveforms side by side. Ask the room what's wrong before you say anything.

**Where they get stuck:**

1. **Verilator 4.** Ubuntu 22.04's apt gives 4.038, which doesn't have `--binary` or
   `--timing`. Have everyone run `verilator --version` at kickoff, not on day 9.
2. **Warnings stop the build.** `write_data = i;` in the SRAM testbench (a 32-bit `int` into
   8 bits) fails with `WIDTHTRUNC`. The fix is `i[7:0]`. Expect this on every Exercise 4
   attempt.
3. Editing a `.sv` file and rerunning `./obj_dir/Vtest` without recompiling, then deciding
   the fix "didn't work."
4. Changing inputs on `@(posedge clk)` instead of `@(negedge clk)`, which gives off-by-one
   waveforms that look like design bugs.
5. Testbenches that never assert reset. Verilator starts every signal at 0, so the counter
   looks fine anyway. The optional "second simulator" section at the end of Lesson 1 is
   built around this.
6. GTKWave on Windows 10 without an X server. Have the Surfer link ready.

**The planted bugs** (the golden folders are the reference solutions):

| Exercise | File | Bug |
|---|---|---|
| 2 | `buggy_counter/buggy_design/counter.sv` | Reset polarity flipped: `if (rst_n)` instead of `if (!rst_n)` |
| 2 | same | Reset value is `4'd5`, not `4'd0` |
| 4 | `buggy_counter_sram/buggy_design/counter_sram.sv` | Counter enable flipped: `else if (!en)` |
| 4 | same | SRAM clocked on `negedge clk` instead of `posedge` |
| 4 | same | SRAM write enable flipped: `if (!write_en)` |

The first bug in each design is loud and hides the others: the counter sits at 5, and the
address sits at 0. The lessons tell members how many bugs each design has and give three
levels of hints, so everyone should find all five. In review, check that the write-up names
the right line for each one, and note who needed the hints.

**In review, look at:** whether the Exercise 2 testbench was written from scratch (an exact
copy of the golden one gets changes requested), whether it shows wrap-around and a mid-count
reset, and whether they did the "prove it" step, running their testbench against the
original buggy design. The write-up should name lines, not just symptoms.

### Block 3: Physical Design (Oct 19 to Oct 30)

**Demo:** a full run takes too long to do live. Start a run at the beginning of the demo,
talk over it, and have a finished run directory open in another window to show the outputs.
Then open KLayout and toggle layers.

**Where they get stuck:**

1. **Environment.** This block is mostly environment problems. Sort out machine access in
   September, not on October 19. Anyone who can't run Nix locally needs a lab machine
   reserved before the block opens.
2. Running `librelane` outside `nix-shell`, and getting "command not found."
3. `DESIGN_NAME` not matching the module name.
4. Committing the run directory. Reject any PR with thousands of files right away and point
   them to the `.gitignore`.

**Pre-block dependency:** the Su26LLEX cleanup (nested-directory note in its README, typo
fixes, pinned LibreLane version). Owner: Bryson. If the version isn't pinned, everyone's
numbers differ and the write-ups can't be compared.

**Not yet tested end to end:** the starter `config.yaml` has never been run through the
full flow on `counter_sram`. It borrows the small-design power grid settings from
LibreLane's `spm` example. Run it once on a lab machine and on a student laptop before the
block opens, and fix the config if the floorplan or power grid steps complain.

**In review, look at:** whether the metrics table came from their own run or a neighbor's.
Once people do the "turn a knob" lesson, their numbers should differ a little.

---

## 6. PR review

Review within 72 hours of the PR opening. A member who waits a week for a review learns that
deadlines only apply to them, and you won't get that trust back.

**Merge when:** every deliverable is there, it runs, and the write-up is in their own words.

**Request changes when:** something is missing or broken. Be specific and short. "The
waveform screenshot doesn't show a pedestrian press. Can you add one?" is a good review. A
paragraph of encouragement wrapped around a vague concern is not.

**Never** leave "looks good" on work that doesn't. The rotation is how we place people, and
inflated reviews break it.

Keep a running spreadsheet: member, block, on time (Y/N), a quality note, and which team they
seemed to enjoy. That spreadsheet is what we bring to placement week.

## 7. Stragglers

The completion bar is firm. The person we worry about is the one who hits an install problem
in week one, goes quiet, and never comes back.

- If someone hasn't asked a question or opened a PR by Wednesday of week two, a lead messages
  them directly. Not a group ping.
- Late with notice is fine. We chase silence.
- Missing one block doesn't end the rotation. Missing two does. Talk to them about joining in
  spring instead.

## 8. Placement week (Nov 2)

Members rank all three teams. Leads bring the spreadsheet. Where a member's choice and the
leads' read agree, it's automatic. Where they differ, the member's choice wins. The rotation
is there to inform their choice, not to override it.

If a team ends up badly under-subscribed even after rotation, that tells us something about
how we taught that block, not about the members.

## 9. Pre-semester checklist

| Item | Owner | Status |
|---|---|---|
| Confirm rotation order (Digital, Verification, Physical) with Dr. Limbrick | Zach | |
| Su26LLEX cleanup: nested-directory note, typos, pinned LibreLane version | Bryson | |
| Verify setup installs clean on Ubuntu 24.04, macOS, and WSL | | |
| Verify Block 1 end to end on a fresh machine | | |
| Verify Block 2 exercises build with Verilator 5 on Ubuntu 24.04, macOS, and WSL | | |
| Run Block 3 `config.yaml` through the full flow on a lab machine and a student laptop | | |
| Move this repo to an ASIC GitHub organization and turn on PR reviews | | |
| Reserve lab machines for members who can't run LibreLane locally | | |
| Book room and time for three kickoff demos and three open labs | | |
| Pin a "how to ask a question" post in the GroupMe | | |
| Recruit and brief the three teaching leads | | |

## 10. What to tell Dr. Limbrick

The short version, if you have three minutes with him:

> Every new member does three two-week projects, one each in digital design, verification,
> and physical design, before choosing a team. We rotate instead of letting people
> self-select because Silicon Jackets found self-selection sends two thirds of members to
> digital design. The projects build directly toward the tapeout: the design block uses the
> Tiny Tapeout pin contract, the verification block has members write testbenches and hunt
> planted bugs, and the physical design block runs the same LibreLane sky130 flow we submit
> with. Everything is turned in as a pull request on GitHub, which gives us a record of who
> finished what and gives every member public commits on a chip design project. What we
> need from you: confirmation on the rotation order, lab machine access for members who
> can't run the tools on their own laptops, and your read on whether the completion bar is
> where you'd set it.
