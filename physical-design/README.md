# Block 3 — Physical Design: Counter to Layout

**Two-week rotation block. Oct 19 – Oct 30.**

Run the LibreLane tutorial once, then repeat the same process on your own 8-bit counter,
from code to a finished layout. Pull it up in KLayout and grab a screenshot. Turn in the
layout files, the screenshot, and a few sentences on what each step did.

---

## Why this project

Everything up to now has been text that describes hardware. This block is where the text
becomes geometry — actual rectangles of metal and silicon at specific coordinates, which
is what a foundry can build.

This is also the block where members find out whether they like this work. Physical
design has a different rhythm than RTL: you are not writing much, you are configuring a
flow, reading reports, and reacting to what the tools tell you. Some people love it and
some people bounce off it. Both answers are useful for placement.

The output of this block is a `.gds` file. That is the same file format we submit to
Tiny Tapeout in December. This is not a simulation of the process. It is the process.

---

## What "hardening" actually means

You are running a sequence of tools, each of which takes the previous one's output and
adds physical detail. Learn these six names now — they are what the whole industry calls
these steps, and you will be asked about them in an internship interview.

| Stage | Tool | What it does | What comes out |
|---|---|---|---|
| **Synthesis** | Yosys | Turns your Verilog into a netlist of actual sky130 standard cells — specific AND gates, flip-flops, buffers that the foundry can build | Gate-level netlist |
| **Floorplan** | OpenROAD | Decides how big the chip is, where the I/O pins sit, and lays down the power grid | Die and core area, PDN |
| **Placement** | OpenROAD | Assigns every one of those cells an actual x,y position in a row | Placed netlist |
| **CTS** | OpenROAD | Builds a clock distribution tree so the clock edge arrives at every flip-flop at nearly the same time | Clock tree, buffers inserted |
| **Routing** | OpenROAD | Draws the metal wires connecting everything, across five metal layers | Routed design |
| **Signoff** | OpenROAD / Magic / KLayout / Netgen | Checks timing (STA), design rules (DRC), and that the layout matches the netlist (LVS) | Reports, and `.gds` |

Your write-up at the end is you explaining these six rows in your own words, using
numbers from your own run.

---

## Step by step

### Step 1 — Run the tutorial exactly as written, change nothing

```bash
cd ~/Su26LLEX
```

Follow the README start to finish on the example design it ships with. Do not swap in
your own RTL yet. Do not change any config values. The only goal of this step is to
prove your toolchain works.

If it fails here, it is an environment problem, not a design problem, and those are two
completely different conversations. Post in `#help` with the full error.

> **The folder thing:** `Su26LLEX` is a fork of LibreLane, so there is a `librelane/`
> directory inside it, and tutorial paths look like `librelane/examples/...`. That is
> correct even though it looks like a mistake.

When it finishes, find the run directory. It looks like `runs/RUN_2026-10-20_.../` and
contains a numbered folder for every step the flow took. Open it and scroll through the
folder names. That list *is* the flow. Take thirty seconds to look at it before moving
on — it is the clearest picture of the process you will get.

### Step 2 — Set up your own design

```bash
cd ~/silicon-aggies-onboarding
mkdir -p submissions/physical-design/YOUR-GITHUB-USERNAME/src
cd submissions/physical-design/YOUR-GITHUB-USERNAME

cp ../../../physical-design/starter/config.json .
cp ../../verification/YOUR-GITHUB-USERNAME/tt_um_counter.v src/
```

That second copy is your **fixed** counter from Block 2 — the one you debugged. If you
harden the broken one, you get a perfectly manufacturable broken chip, which is a real
thing that happens to real companies.

### Step 3 — Read the config before you run it

Open `config.json`. Four values matter:

- **`CLOCK_PERIOD`** — the target period in nanoseconds. 20 ns is about 50 MHz, deliberately
  slack. Tighten it later.
- **`FP_CORE_UTIL`** — what percentage of the core area gets filled with cells. Higher is
  denser and smaller; too high and the router runs out of room and fails.
- **`PL_TARGET_DENSITY_PCT`** — placement density. Usually kept a bit below core util.
- **`VERILOG_FILES`** — must point at your file. `dir::` means "relative to this config."

Change nothing yet. Run it stock first so you have a baseline.

### Step 4 — Run the flow

From inside the LibreLane environment (see the Su26LLEX README for the exact invocation
for the version we pinned — usually a `nix-shell` then the `librelane` command):

```bash
librelane config.json
```

Expect several minutes. It will print each stage as it goes. Watch which stage takes
longest — that answer is different than most people guess.

### Step 5 — Read the reports, not just the pass/fail

This is the actual skill. Go into your run directory and fill in this table for your
write-up:

| Metric | Where to find it | Yours |
|---|---|---|
| Die area (µm²) | final metrics summary | |
| Standard cell count | synthesis report | |
| Flip-flop count | synthesis report | |
| Worst negative slack (WNS) | STA report | |
| Total negative slack (TNS) | STA report | |
| Number of nets routed | routing report | |
| DRC violations | signoff DRC report | |
| LVS result | signoff LVS report | |

LibreLane collects most of these into a metrics file in the `final/` directory. Find it.
The point of this step is that you learn where the numbers live, because for the rest of
your career in this field, someone is going to ask you "what's the WNS?" and you need to
be able to answer in under a minute.

**WNS should be positive or zero.** Positive slack means the design meets timing with
room to spare. Negative means a path is too slow for your clock period and the design
would not work at that frequency.

### Step 6 — Open it in KLayout

```bash
klayout runs/RUN_<your-timestamp>/final/gds/tt_um_counter.gds
```

Give it a moment. Then:

- Turn layers on and off in the right-hand panel. Find the metal layers (met1 through
  met5) and toggle them one at a time. You are looking at the actual wires.
- Zoom all the way in until you can see individual standard cells. Those repeating
  rectangles in rows are your flip-flops and gates.
- Zoom all the way out. That whole thing is your 8-bit counter.

Screenshot it — a full-chip view with all layers on. Save as `layout.png`.

Take a second screenshot zoomed in far enough to see individual cells. Save it as
`layout-zoom.png`. That one is the picture that makes the point to a person who has never
seen this before, which makes it useful for recruiting.

### Step 7 — Now change one thing and rerun

Pick one:

- Drop `CLOCK_PERIOD` from 20 to 5 and see whether timing still closes.
- Raise `FP_CORE_UTIL` from 40 to 70 and see what happens to area and to routing.

Rerun. Record what changed in the metrics table. One or two sentences on what you learned
goes in the write-up.

This step is the difference between "I ran a tutorial" and "I understand what the knobs
do."

### Step 8 — Write it up

`WRITEUP.md`, 300–500 words:

- One or two sentences per stage, in your own words, on what that stage did to your
  design. Reference your own numbers.
- Your filled-in metrics table.
- What you changed in Step 7 and what happened.
- What surprised you.

Do not paraphrase this README back at us. Leads can tell, and the whole value of the
exercise is in you forming your own description.

### Step 9 — Open the pull request

```bash
cd ~/silicon-aggies-onboarding
git checkout -b block3-yourname
git add submissions/physical-design/YOUR-GITHUB-USERNAME
git commit -m "Block 3: counter to layout"
git push -u origin block3-yourname
```

> **Do not commit the whole run directory.** It is hundreds of MB. Commit the final GDS,
> your config, your RTL, the screenshots, and the metrics — nothing from intermediate
> stages. There is a `.gitignore` in the repo root that handles this; if `git status`
> shows thousands of files, stop and ask.

---

## Deliverables

In `submissions/physical-design/YOUR-GITHUB-USERNAME/`:

- [ ] `src/tt_um_counter.v` — the RTL you hardened
- [ ] `config.json` — your config, including the Step 7 change
- [ ] `tt_um_counter.gds` — the final layout
- [ ] `layout.png` — full-chip KLayout screenshot
- [ ] `layout-zoom.png` — zoomed-in screenshot showing individual cells
- [ ] `metrics.md` — the filled-in table from Step 5, both runs
- [ ] `WRITEUP.md` — 300–500 words
- [ ] PR opened by **Friday Oct 30, 11:59 PM**

## Definition of done

- The flow completes through signoff with zero DRC violations and LVS clean.
- WNS is non-negative at your stated clock period.
- Both screenshots are legible.
- The write-up describes all six stages using your own numbers.

---

## Common problems

| Symptom | What is usually wrong |
|---|---|
| Nix install fails or runs out of disk | You need ~15 GB free. Use a lab machine — arrange it with a lead *before* the block starts |
| Flow fails in synthesis | Your Verilog has something non-synthesizable in it. Delays (`#10`), `initial` blocks, and `$display` are simulation-only |
| "no cells placed" / floorplan errors | `DESIGN_NAME` does not match your module name, or `VERILOG_FILES` path is wrong |
| Routing fails or takes forever | `FP_CORE_UTIL` too high. Drop it back toward 40 |
| Negative WNS | Your `CLOCK_PERIOD` is too aggressive for the design. Raise it, then note in the write-up what the fastest closing period was |
| Antenna violations | Common and usually fixable by the flow's own diode insertion. Note them, ask a lead |
| KLayout opens a blank window | You opened the wrong file, or all layers are hidden. Check the layer panel on the right |
| `git status` shows thousands of files | You are about to commit the run directory. Do not. See the note in Step 9 |

## If you finish early

1. Harden your Block 1 traffic light controller instead and compare the two — which is
   bigger, and does the answer match your intuition from the RTL?
2. Find the critical path in the STA report and trace it back to specific lines of your
   Verilog.
3. Sweep `CLOCK_PERIOD` across five values, plot area against achieved frequency, and you
   have built a two-point Pareto curve. That is exactly the shape of the Code-a-Chip
   notebook work the org is submitting to ISSCC — come talk to us.
