# Troubleshooting (Block 3)

Look for your problem here before you ask in the GroupMe.

If it isn't here, post the command you ran, the last 20 or so lines of output (copy and
paste them, don't send a photo), and your operating system. When the flow fails, the name
of the step that failed is in those last lines. Include it.

Most problems in this block are about the tools, not your design. That's normal.

---

## Installing and starting

**Nix install fails, or you run out of disk space**
You need about 20 GB free. If your laptop doesn't have room, or Nix won't install, tell a
lead so you can work out another option. Do this before the block starts if you can.

**`nix-shell` takes forever the first time**
The first run downloads the whole toolchain, which can take 10 to 40 minutes. If it seems
to be *building* things (lots of lines with "building" and compiler output) for more than
an hour, Nix isn't using the prebuilt download server. Ask a lead. It usually means Nix was
installed without the extra settings in setup Part D1.

**`librelane: command not found`**
You're not inside the LibreLane environment. Run `nix-shell ~/Su26LLEX/shell.nix` first. You
need to do this in every new terminal.

**`nix-shell: command not found`**
Nix isn't installed, or you didn't open a new terminal after installing it. Close the
terminal, open a new one, and try again. If it's still missing, redo setup Part D1.

**`error: getting status of '/home/.../Su26LLEX/shell.nix': No such file or directory`**
The tutorial repo isn't in your home folder. Run `cd ~` and then
`git clone https://github.com/bdawgcodes28/Su26LLEX.git` (setup Part D2).

---

## The flow fails

**Fails at the very start, complaining about a config variable**
There's a typo in `config.yaml`. Setting names are all capitals and must be spelled exactly.
Each line is `NAME: value`, with a space after the colon.

**Fails in synthesis, or in the linter step at the start**
Something in your Verilog can't be built into hardware. Testbench-only commands like `#10`,
`initial`, `$display`, and `$finish` can't be in a design. Make sure `src/counter_sram.sv`
is your design, not your testbench.

**"no cells", "module not found", or "top module" errors**
`DESIGN_NAME` in `config.yaml` doesn't match the `module` line in your design, or
`VERILOG_FILES` points to the wrong file. Both should say `counter_sram`.

**Fails in the floorplan or power grid (PDN) step**
The chip is too small for the power grid settings. Ask a lead. This config hasn't been run
on every laptop yet, and a lead may need to adjust the `PDN_` lines.

**Routing fails, or runs for a very long time**
`FP_CORE_UTIL` is too high, so the cells are packed too tightly to fit the wires. Lower it
back toward 40.

**Negative WNS (timing not met)**
`CLOCK_PERIOD` is too short for this design. Make it longer. If you're doing Option A in
Lesson 5, this is an interesting result, not a failure: find the shortest clock period that
still gives WNS of zero or more, and put that in your write-up.

**Antenna warnings or violations**
These are common. The flow usually fixes them itself by adding small diodes. Note them in
your write-up and mention them to a lead.

**I reran with the same run tag, and now there are two synthesis folders (or the numbers look doubled)**
LibreLane doesn't warn you when you reuse a run tag. It quietly adds the new run's steps to
the end of the old run's folder and keeps numbering from where it stopped, so `runs/first`
ends up with two `yosys-synthesis` folders, and `final/` holds whichever run came last. Lesson
3's commands then read both reports at once.

Fix it by starting that run over cleanly. Add `--overwrite` to the same command, which
deletes the old folder first:
`librelane config.yaml --run-tag first --overwrite`
Or use a new tag, like `--run-tag second`, and use that name in every later command.

---

## KLayout

**KLayout won't open (Windows 10)**
WSL on Windows 10 can't open windows without extra setup. Use a Windows 11 or Mac laptop
(a friend's is fine) for Lesson 4, or tell a lead early.

**KLayout shows only a few empty boxes with names in them**
Press `*` (or **Display**, then **Full Hierarchy**) to draw everything inside the cells.

**KLayout opens, but the window is blank**
All the layers may be hidden. Right-click the layer panel on the right and choose
**Show All**, then press F2 to fit. If it's still blank, check that you opened
`counter_sram.gds` from the `final/gds` folder.

---

## Git

**`git status` shows thousands of files, or files inside `runs/`**
Stop. You're about to commit the run folder. Make sure you're in `~/silicon-aggies-onboarding`
and that `.gitignore` is there (`ls -a`). Only add your submission folder:
`git add submissions/physical-design/YOUR-GITHUB-USERNAME`.

**`git show block2-...` says `fatal: invalid object name`**
The branch name is wrong. Run `git branch` to see your branches.

For anything else about git, see the git section of
[Block 1's troubleshooting page](../digital-design/TROUBLESHOOTING.md#git-and-github).
