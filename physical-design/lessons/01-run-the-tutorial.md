# Lesson 1: Run the tutorial

**Goal:** run the ASIC LibreLane tutorial exactly as written, on the example design it comes
with. You don't change anything. The only point of this lesson is to prove your tools work.

If something fails here, it's a problem with your setup, not with any design. Post in the
GroupMe with the full error.

---

## Step 1: Start the LibreLane environment

```bash
nix-shell ~/Su26LLEX/shell.nix
```

The first time you ran this in setup, it took a long time. Now it should take a few seconds.
When it's ready, your prompt starts with `[nix-shell`.

**You have to be inside this environment for every LibreLane command in this block.** If you
open a new terminal, run `nix-shell ~/Su26LLEX/shell.nix` again first. When you're done for
the day, type `exit` to leave it.

## Step 2: Follow the tutorial

Open the tutorial's README on GitHub: <https://github.com/bdawgcodes28/Su26LLEX>. It's also
on your computer at `~/Su26LLEX/Readme.md`.

Skip its installation and cloning sections, since you did those in setup. Start at
**"Running Default LibreLane Flow."** Here's the short version of what it has you do:

```bash
cd ~/Su26LLEX/librelane/examples/test_sram_macro
ls
librelane config.json --run-tag tutorial
```

`--run-tag tutorial` names this run "tutorial," so its results go in a folder called
`runs/tutorial`.

The run takes several minutes. It prints each stage as it goes, with a step number. Watch
which stage takes the longest. It's probably not the one you'd guess.

When it finishes, the last lines should say the flow completed. If it stops with an error
instead, copy the last 20 or so lines and post them in the GroupMe.

## Step 3: Look at the run folder

```bash
cd runs/tutorial
ls
```

You'll see a long list of numbered folders, like `01-verilator-lint`,
`06-yosys-synthesis`, `12-openroad-floorplan`, and so on. There's one folder for every step
the flow took, in order.

Scroll through the names. That list is the flow. Try to find the six stages from Lesson 0 in
it: synthesis, floorplan, placement, clock tree (`cts`), routing, and the signoff checks
near the end (`drc`, `lvs`, `sta`).

The `final` folder holds the finished results.

## Step 4: Open the layout

Still inside `runs/tutorial`:

```bash
cd final/klayout_gds
klayout test_sram_macro.klayout.gds
```

KLayout opens and shows the layout. The two big blocks are the SRAM memories. The rest is
the logic around them, plus the wires connecting everything. You'll learn to use KLayout
properly in Lesson 4. For now, just check that it opens.

Close KLayout when you're done.

---

## Before you move on

- [ ] `nix-shell` starts, and `librelane` runs inside it.
- [ ] The tutorial run finished without errors.
- [ ] You found the six stages in the run folder names.
- [ ] KLayout opened the tutorial's layout.

---

**Next:** [Lesson 2: Harden your design](02-harden-your-design.md).
