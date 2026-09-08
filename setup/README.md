# Setup — Do This Before September 17

Install night is the interest meeting on **Thursday, September 17**. Get as far as you
can before then and bring your laptop with whatever broke. Leads will be in the room.

Budget about 90 minutes. The LibreLane piece (Part D) is the slow one and you do not need
it until Block 3 — but install it early so failures surface in September, not October.

---

## Part 0 — What OS you are on

| Your machine | What to do |
|---|---|
| Windows | Install WSL2 with Ubuntu and do **everything** inside it. Do not use PowerShell, Git Bash, or Cygwin. |
| macOS (Apple Silicon or Intel) | Use Terminal directly. Install Homebrew first. |
| Linux | You are already fine. |
| A Chromebook or a tablet | Talk to a lead. We will get you on a lab machine. |

**Windows — WSL2 install.** Open PowerShell *as Administrator* and run:

```powershell
wsl --install -d Ubuntu
```

Reboot. Open the "Ubuntu" app from the Start menu, set a username and password (the
password will not show characters as you type — that is normal). Every command in the
rest of this repo goes in that Ubuntu window.

Keep your work inside the Linux filesystem (`/home/yourname/`), not `/mnt/c/`. Tools run
several times slower across the Windows filesystem boundary and some of them break
outright.

---

## Part A — Git and GitHub

```bash
# Ubuntu / WSL2
sudo apt update && sudo apt install -y git

# macOS
brew install git
```

Configure it once:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@aggies.ncat.edu"
```

Then:

1. Make a GitHub account if you do not have one. Use your `@aggies.ncat.edu` address —
   it gets you the free GitHub Student Developer Pack.
2. Go to the Silicon Aggies onboarding repo and click **Fork** (top right).
3. Clone *your fork*:

```bash
git clone https://github.com/YOUR-USERNAME/silicon-aggies-onboarding.git
cd silicon-aggies-onboarding
```

4. Add the org repo as `upstream` so you can pull updates:

```bash
git remote add upstream https://github.com/silicon-aggies/silicon-aggies-onboarding.git
git remote -v          # should list both origin and upstream
```

**If you have never used git:** the four commands that cover 95% of what you need are
`git status`, `git add .`, `git commit -m "message"`, `git push`. There is a five-minute
git primer in `LEADS.md` that leads walk through at the kickoff.

---

## Part B — Simulation (Blocks 1 and 2)

Icarus Verilog compiles and runs your design. GTKWave shows you the waveforms.

```bash
# Ubuntu / WSL2
sudo apt install -y iverilog gtkwave

# macOS
brew install icarus-verilog
brew install --cask gtkwave
```

Check it worked:

```bash
iverilog -V | head -1     # expect: Icarus Verilog version 11.0 or newer
gtkwave --version
```

> **WSL2 note:** GTKWave needs a graphical window. On Windows 11 this works out of the
> box through WSLg. On Windows 10 you need an X server (VcXsrv) — ask a lead, or skip it
> and view your `.vcd` files in the [Surfer web viewer](https://surfer-project.org/)
> instead, which needs nothing installed.

---

## Part C — Python and cocotb (Block 2)

```bash
# Ubuntu / WSL2
sudo apt install -y python3 python3-pip python3-venv make

# macOS
brew install python make
```

We use a virtual environment so cocotb does not collide with anything else on your
machine:

```bash
cd ~/silicon-aggies-onboarding
python3 -m venv .venv
source .venv/bin/activate        # you must run this every new terminal session
pip install "cocotb==2.0.1" pytest
```

Check it:

```bash
cocotb-config --version          # must print 2.0.1
```

> **Pin the version, do not upgrade.** cocotb 2.x changed its API from 1.x — for example
> `Timer(1, units="ns")` became `Timer(1, unit="ns")`. Our starter tests are written
> against 2.0.1. If you install a different version, examples from tutorials and from
> Stack Overflow will not match what you have, and neither will the help you get from a
> lead.

When your prompt starts with `(.venv)` the environment is active. If you close the
terminal and come back, run `source .venv/bin/activate` again.

---

## Part D — LibreLane (Block 3)

This is the big one. It pulls down the sky130 process design kit and a full open-source
EDA toolchain. Expect 20–40 minutes and several GB.

We install it through Nix, which is what LibreLane upstream recommends and what makes
everyone's environment identical.

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

Close and reopen your terminal, then:

```bash
nix --version
```

Then clone the Silicon Aggies LibreLane tutorial repo:

```bash
cd ~
git clone https://github.com/bdawgcodes28/Su26LLEX.git
cd Su26LLEX
```

Follow that repo's README from there. It pins a specific LibreLane version on purpose —
do not upgrade past it mid-semester, or your results stop matching everyone else's.

> **Heads up on the folder structure:** `Su26LLEX` is itself a fork of LibreLane, so
> there is a `librelane/` directory *inside* it. That looks wrong the first time you see
> it. It is not. The tutorial paths like `librelane/examples/...` are correct.

**If Nix fails or the download is too large for your machine**, we have a fallback: lab
machines in the ADEPT lab have the toolchain preinstalled, and there is a Docker path
documented in the Su26LLEX README. Tell a lead which one you need before Block 3 starts,
not during it.

---

## Part E — An editor

Use whatever you like. If you have no preference, VS Code with these extensions:

- **WSL** (Windows only — lets VS Code edit files inside Ubuntu)
- **Verilog-HDL/SystemVerilog** by mshr-h — syntax highlighting and linting
- **Python** — for cocotb tests

---

## Verify everything at once

Save this as `check.sh` in the repo root and run `bash check.sh`:

```bash
#!/usr/bin/env bash
echo "--- git ---";      git --version           || echo "MISSING"
echo "--- iverilog ---"; iverilog -V | head -1   || echo "MISSING"
echo "--- gtkwave ---";  gtkwave --version 2>&1 | head -1 || echo "MISSING"
echo "--- python ---";   python3 --version       || echo "MISSING"
echo "--- cocotb ---";   cocotb-config --version || echo "MISSING (activate .venv?)"
echo "--- nix ---";      nix --version           || echo "MISSING (needed for Block 3)"
```

Bring the output of that to install night if anything says MISSING.
