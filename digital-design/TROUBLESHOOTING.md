# Troubleshooting

Check here before posting in `#help`. There's a good chance your error is below.

If it isn't, post with **what you ran**, **the full error text** (copy-paste, not a
photo), and **your OS**.

---

## Tools won't install or run

**`iverilog: command not found`**
Not installed, or you're in the wrong shell. On Windows, everything happens inside the
Ubuntu window, never PowerShell or Git Bash. See [`../setup/README.md`](../setup/README.md).

**`make: command not found`**
`sudo apt install make` on Ubuntu/WSL2, `brew install make` on macOS.

**GTKWave opens nothing / won't launch (Windows)**
WSLg isn't available on Windows 10. Two options: install VcXsrv as an X server, or skip
GTKWave entirely and upload your `.vcd` to [Surfer](https://surfer-project.org/) in your
browser. Same information, nothing to install.

**Everything is painfully slow (Windows)**
You're probably working under `/mnt/c/`. Move your work into the Linux filesystem —
`~/silicon-aggies-onboarding`. Crossing the Windows filesystem boundary is several times
slower and occasionally breaks tools outright.

---

## Compile errors

**`syntax error` on a line that looks fine**
You forgot `-g2012`. Use `make`, which includes it. If you're calling iverilog by hand:
`iverilog -g2012 -o sim.out tb_traffic_light.v tt_um_traffic_light.v`

**A wall of errors**
Read the **first** one only. The rest are almost always fallout. Fix the first, recompile.

**`identifier not declared`**
Typo in a signal name, or you used a signal you never declared. Verilog is case-sensitive:
`ped_req` and `ped_Req` are different signals.

**`cannot perform procedural assignment to a net`**
You assigned to something declared `wire` inside an `always` block. It needs to be `reg`.

**`port not connected` warnings**
Usually harmless here. If it's a real port you meant to use, check your spelling.

---

## Simulation problems

**`TIMEOUT -- the light never reached a state the test was waiting for`**
Your design never turns green (or never leaves a state). If you just copied the starter,
that's expected — fill in the TODOs. If you've written code, your state machine is stuck:
check that every state has a way out and that you cleared the timer on transitions.

**Everything is `x` in the waveform, forever**
A register with no reset path, or you never assigned to it at all. Every `reg` needs a
value in the `if (!rst_n)` branch.

**Test 2 fails, timing off by one** — green is 11 or 13 instead of 12
The `- 1`. Your timer starts at 0, so counting to `GREEN_TIME - 1` gives you exactly
`GREEN_TIME` ticks. Comparing against `GREEN_TIME` gives you one too many.

**The light flickers rapidly between two states**
You changed state on some path but didn't clear the timer. Every transition needs
`timer <= 0`.

**Test 4 fails: "an early press is REMEMBERED..." and green lasted 12**
Your button press is being dropped. You're testing `ped_button` directly somewhere instead
of a latched `ped_req`. The pulse is one tick long and gone. Re-read the latching section
in [Lesson 2](lessons/02-state-machines.md).

**Test 3 fails: a mid-green press doesn't cut green short**
Either the same latching problem, or your GREEN exit condition only checks the timer. It
needs *two* reasons to leave: timer expired, **or** request pending and min-green met.

**Test 5 fails: a press during red shortens the next green**
`ped_req` isn't being cleared during RED, so it's still set when green starts.

**Test 6 fails: one-hot violation**
Two lights on at once, or none. Almost always because outputs are stored in separate
registers instead of derived from `state`. Drive them with
`assign uo_out[2] = (state == S_GREEN);` and the problem disappears by construction.

**Results change between runs**
Shouldn't happen here. If it does, you probably mixed `=` and `<=` in a clocked block.
Use `<=` everywhere inside `always @(posedge clk)`.

---

## Waveform problems

**GTKWave window is empty**
You opened it but haven't added signals. Click the module in the top-left panel, select
signals in the panel below, click **Append**. Then **Shift+Alt+F** to zoom to fit.

**No `.vcd` file exists**
Run `make` first. The simulation has to run before there's anything to view.

**The waveform is a solid block of color**
You're zoomed out too far. Shift+Alt+F, then zoom in with the magnifier buttons.

---

## Git and GitHub

**`git push` asks for a password and then rejects it**
GitHub stopped accepting account passwords. You need a personal access token: GitHub →
Settings → Developer settings → Personal access tokens → Fine-grained tokens. Give it repo
access, then use the token as your password. Or set up SSH keys.

**`git push` says "rejected" or "does not appear to be a git repository"**
You're pushing to the org repo instead of your fork. Run `git remote -v` — `origin` should
be *your* username. If not, see [`../setup/README.md`](../setup/README.md).

**`git status` shows thousands of files**
You're about to commit simulation output. Make sure the repo's `.gitignore` is present and
that you're running git from the repo root, not from somewhere unexpected.

**I committed to `main` by accident**
Not a disaster. Post in `#help`, a lead will walk you through moving it to a branch. Don't
try to fix it with commands you found online — that's how small problems become big ones.

---

## Still stuck

Post in `#help`. Include what you ran, the full error, and your OS.

Nobody here thinks less of you for asking. Most of us learned this six months ago and hit
every single error on this page.
