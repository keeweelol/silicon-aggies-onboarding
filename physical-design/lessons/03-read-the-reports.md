# Lesson 3: Read the reports

**Goal:** find the numbers that tell you whether your chip works, how big it is, and whether
the factory could build it.

Anyone can get a flow to finish. Reading what the tools report is the actual skill. At an
internship, someone will ask you "what's the worst slack?" and expect an answer within a
minute. This lesson is how you learn where to look.

---

## Step 1: Make your metrics file

In your submission folder, create a file called `metrics.md`:

```bash
cd ~/silicon-aggies-onboarding/submissions/physical-design/YOUR-GITHUB-USERNAME
nano metrics.md
```

Paste this table in, save with Ctrl+O and Enter, and quit with Ctrl+X. You'll fill it in as
you go, and add a second column in Lesson 5.

```markdown
# Metrics

| Metric | Run: first |
|---|---|
| Flip-flops (my prediction) | |
| Flip-flops (from synthesis) | |
| Total cells | |
| Die area (µm²) | |
| Worst slack, WNS (ns) | |
| Total negative slack, TNS (ns) | |
| Worst hold slack (ns) | |
| Total wire length (µm) | |
| DRC errors (router, Magic) | |
| DRC errors (KLayout) | |
| LVS errors | |
```

Put your flip-flop prediction from Lesson 2 in the first row now.

## Step 2: Count the flip-flops in the synthesis report

Synthesis writes a report listing every cell it used. Find it:

```bash
ls runs/first/*yosys-synthesis/reports/
```

Open `stat.rpt` from that folder. The `*` in the path fills in the step number for you:

```bash
less runs/first/*yosys-synthesis/reports/stat.rpt
```

(`less` lets you scroll with the arrow keys. Press `q` to quit.)

You'll see a list of cell names with a count next to each, like
`sky130_fd_sc_hd__and2_1   12`. Every name starts with `sky130_fd_sc_hd__`, the name of
the cell library. The part after that is the cell type.

Flip-flop cells have `df` in their name, like `dfxtp` (a plain D flip-flop). To list only
those lines:

```bash
grep df runs/first/*yosys-synthesis/reports/stat.rpt
```

Add up the counts of all the flip-flop cells and put the total in your table. Does it match
your prediction? If not, work out why. A difference usually means you missed a register,
or the tools found one they could remove.

## Step 3: Get the rest from the metrics summary

The flow collects almost every number it measured into one file, `final/metrics.csv`. It
has hundreds of lines, so pull out just the ones you need:

```bash
grep -E "^(design__instance__count|design__die__area|timing__setup__ws|timing__setup__tns|timing__hold__ws|route__wirelength|route__drc_errors|magic__drc_error__count|klayout__drc_error__count|design__lvs_error__count)," runs/first/final/metrics.csv
```

It prints lines like `design__die__area,12345.6`: the name of the metric, a comma, and its
value. Here's what each one means and where it goes in your table:

| Metric in the file | Row in your table | What it means |
|---|---|---|
| `design__instance__count` | Total cells | How many standard cells are in the design, of every kind |
| `design__die__area` | Die area | How big the whole chip is, in square micrometers |
| `timing__setup__ws` | WNS | Worst slack: the least spare time on any path (see below) |
| `timing__setup__tns` | TNS | Total negative slack: all the negative slack added up |
| `timing__hold__ws` | Worst hold slack | The same idea as WNS, but for the opposite problem: a signal arriving *too early*, before the flip-flop has finished grabbing the previous value |
| `route__wirelength` | Total wire length | How much metal wire the router drew, in micrometers |
| `route__drc_errors` and `magic__drc_error__count` | DRC errors (router, Magic) | Places where the layout breaks the factory's rules. The first is the router's own count, the second is Magic's final check. Write both numbers, like `0, 0` |
| `klayout__drc_error__count` | DRC errors (KLayout) | The same check, done a second time by a different tool. Signoff runs both, and both need to be 0 |
| `design__lvs_error__count` | LVS errors | Places where the layout doesn't match the netlist |

If a metric isn't printed, that step may have been skipped, or its name is slightly
different in your LibreLane version. Run `grep drc runs/first/final/metrics.csv` (or `lvs`,
or `timing__setup`) to look for close matches, and ask in the GroupMe if you can't find it.

## Step 4: Understand slack

**Slack** is how much spare time a signal has. A signal leaves a flip-flop on one clock
edge and has to reach the next flip-flop before the following edge.

- If it arrives with 3 ns to spare, the slack on that path is +3 ns.
- If it arrives 1 ns late, the slack is -1 ns, and the chip wouldn't work at that clock
  speed.

**WNS (worst negative slack)** is the slack on the slowest path in the whole design.

- **WNS zero or positive:** timing is met. Every path makes it in time.
- **WNS negative:** at least one path is too slow for your clock period.

With a 20 ns clock, your WNS should be comfortably positive. In Lesson 5 you'll shrink the
clock period and see what happens to it.

## Step 5: Check the must-pass numbers

For your design to count as done, these need to be true:

- [ ] DRC errors: **0** in all three counts (router, Magic, and KLayout)
- [ ] LVS errors: **0**
- [ ] WNS: **zero or positive**

Also look at the worst hold slack. It should be zero or positive too. If it's negative, the
flow normally stops on its own before it gets this far. If it didn't, tell a lead.

If any of these fail, check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) and post in the
GroupMe.

---

## Before you move on

- [ ] `metrics.md` has every row filled in for the `first` run.
- [ ] You compared your flip-flop prediction to the synthesis report.
- [ ] You can explain what WNS means in one sentence.

---

**Next:** [Lesson 4: Look at the layout](04-look-at-the-layout.md).
