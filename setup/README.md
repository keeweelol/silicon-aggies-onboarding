# Setup: install everything once

This guide gets your computer ready for all three blocks. Plan on about an hour and a half.
Most of that is waiting for downloads.

Do Parts 0 through C before Block 1. Part D (LibreLane) is only needed for Block 3, but
it's the biggest download and the most likely to break, so install it early. That way
problems show up while there's still time to fix them.

If you get stuck anywhere, stop and post in the ASIC GroupMe with the command you ran and
the full error text. Don't skip a step and hope it works out later.

---

## Part 0: Which computer are you on?

| Your computer | What to do |
|---|---|
| Windows | Install WSL (below). You'll do **everything** for ASIC inside it. |
| Mac | Use the Terminal app. Install Homebrew (below). |
| Linux | You're ready. Use Ubuntu 24.04 or newer if you can. |
| Chromebook or tablet | Talk to a lead early so we can figure out a computer you can use. |

You need about 20 GB of free disk space and at least 8 GB of RAM.

### Windows: install WSL

WSL (Windows Subsystem for Linux) runs a real copy of Ubuntu Linux inside Windows. Chip
design tools are built for Linux, so this is how you get them on a Windows laptop.

1. Click Start, type **PowerShell**, right-click it, and choose **Run as administrator**.
2. Paste this and press Enter:

   ```powershell
   wsl --install -d Ubuntu-24.04
   ```

3. Restart your computer when it asks.
4. Click Start and open **Ubuntu 24.04**. The first time, it asks you to make a username
   and password. When you type the password, nothing shows up on screen. That's normal.
   Type it anyway and press Enter. Remember this password; you'll need it often.

From now on, **every command in this repo goes in that Ubuntu window**, not PowerShell and
not Git Bash. If you're ever unsure which window you're in, the Ubuntu one shows a prompt
like `yourname@DESKTOP-ABC123:~$`.

> **Already had WSL before this?** Check which Ubuntu you have by running `lsb_release -a`
> in the Ubuntu window. If it says 22.04, install 24.04 with the command above and use that
> one instead. Block 2 needs a tool version that 22.04 doesn't have.

Keep your work inside the Linux side (your home folder, `~`). Don't work in `/mnt/c/...`,
which is your Windows C: drive. The tools run much slower there, and some don't work at all.

### Mac: install Homebrew

Homebrew is a tool that installs other tools. Open the **Terminal** app (press Cmd+Space
and type "Terminal") and paste:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

It will ask for your Mac password. At the end it prints a "Next steps" section with two or
three commands to run. **Run those**, or `brew` won't work.

---

## How to use the terminal (read this if you never have)

The terminal is a window where you type commands instead of clicking. Every guide in this
repo gives you commands in gray boxes like this:

```bash
cd ~/silicon-aggies-onboarding
ls
```

A few things that help:

- Run commands **one line at a time**, in order. Copy a line, paste it into the terminal,
  press Enter, and wait for it to finish before doing the next one. You know a command is
  done when you see the prompt (the line ending in `$`) again.
- To paste in the Ubuntu window, right-click or press Ctrl+Shift+V. Plain Ctrl+V often
  doesn't work there. On a Mac, Cmd+V works.
- Anything after a `#` in a command box is a note for you to read. You can paste it along
  with the command. The terminal ignores it.
- When you see `YOUR-GITHUB-USERNAME` or `yourname` in a command, replace it with your own
  before pressing Enter.
- `sudo` at the start of a command means "run this as administrator." It asks for the
  password you made earlier. The password stays invisible while you type it.

Four commands you'll use constantly:

| Command | What it does |
|---|---|
| `pwd` | Prints which folder you're in right now |
| `ls` | Lists the files in this folder |
| `cd foldername` | Moves into a folder. `cd ..` goes up one level. `cd ~` goes to your home folder |
| `nano filename` | Opens a file in a simple text editor. Save with Ctrl+O then Enter, quit with Ctrl+X |

`~` is short for your home folder. On Ubuntu it's `/home/yourname`.

---

## Part A: Git and GitHub

Git keeps track of changes to your files. GitHub is the website where the ASIC repo lives
and where you turn in your work.

### A1. Install git and the GitHub command line tool

```bash
# Ubuntu / WSL
sudo apt update
sudo apt install -y git gh

# Mac
brew install git gh
```

### A2. Tell git who you are

Use your real name and the email you'll use on GitHub:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@aggies.ncat.edu"
```

### A3. Make a GitHub account

Go to [github.com](https://github.com) and sign up. Use your `@aggies.ncat.edu` email. That
gets you the free GitHub Student Developer Pack.

### A4. Log in from the terminal

```bash
gh auth login
```

It asks you a few questions. Pick these answers with the arrow keys and Enter:

1. Where do you use GitHub? **GitHub.com**
2. Preferred protocol? **HTTPS**
3. Authenticate Git with your GitHub credentials? **Yes**
4. How would you like to authenticate? **Login with a web browser**

It shows you a one-time code. Copy it, press Enter, and a browser page opens. (On WSL, if
no browser opens, go to <https://github.com/login/device> yourself.) Paste the code and
approve. When the terminal says `Logged in as ...`, you're done.

This step is what lets you upload your work later. Without it, `git push` asks for a
password and then rejects it.

### A5. Fork the ASIC repo

A fork is your own copy of the repo on GitHub. You put your work in your fork, then ask for
it to be added to the main repo.

1. Go to <https://github.com/zjohnson2005/silicon-aggies-onboarding>.
2. Click **Fork** near the top right, then **Create fork**.

### A6. Download your fork to your computer

Replace `YOUR-GITHUB-USERNAME` with your GitHub username:

```bash
cd ~
git clone https://github.com/YOUR-GITHUB-USERNAME/silicon-aggies-onboarding.git
cd silicon-aggies-onboarding
```

Now connect it to the main ASIC repo, so you can pull in new lessons when leads add them:

```bash
git remote add upstream https://github.com/zjohnson2005/silicon-aggies-onboarding.git
git remote -v
```

`git remote -v` should list four lines: two for `origin` (your fork, with your username)
and two for `upstream` (the main repo).

> If the repo moves to an ASIC organization account on GitHub later, leads will post the new
> address and the one command to update it.

---

## Part B: Simulation tools (Blocks 1 and 2)

A simulator runs your hardware design in software so you can see what it would do before
it's a real chip. A waveform viewer draws the results as a picture of signals over time,
which is called a waveform. You'll use GTKWave on Ubuntu and Windows, and Surfer on a Mac. Python and `make` run the Block 1 self-checker.

```bash
# Ubuntu / WSL
sudo apt install -y iverilog gtkwave python3 make

# Mac
xcode-select --install          # Apple's developer tools, which include make
brew install icarus-verilog python surfer
```

(On a Mac, `xcode-select --install` may say the tools are already installed. That's fine.
Don't `brew install make`: Homebrew names it `gmake`, so `make` still isn't found.)

Check they installed:

```bash
iverilog -V | head -1
gtkwave --version      # Ubuntu / WSL
which surfer           # Mac
```

The first should print `Icarus Verilog version 12.0` or newer (11 is fine too). The second
prints a GTKWave version on Ubuntu, or a path ending in `surfer` on a Mac.

> **Why Surfer on a Mac?** Homebrew no longer offers GTKWave for Mac, so don't try
> `brew install --cask gtkwave`. Surfer shows the same waveforms. The lessons are written
> for GTKWave, so wherever they say `gtkwave`, type `surfer`.
>
> **GTKWave on Windows 10:** GTKWave needs to open a window, and WSL on Windows 10 can't do
> that without extra setup. Windows 11 works out of the box. On Windows 10, use the
> [Surfer web viewer](https://surfer-project.org/) instead. You open your waveform file in
> your browser and nothing needs installing.

---

## Part C: Verilator (Block 2)

Verilator is a second simulator. It's faster than Icarus and it's what Block 2 uses. It
works by turning your design into a C++ program, so it also needs a C++ compiler, which is
what `build-essential` installs.

```bash
# Ubuntu / WSL
sudo apt install -y verilator build-essential

# Mac (the compiler comes with Homebrew's install)
brew install verilator
```

Check the version:

```bash
verilator --version
```

It must say **5.0 or higher**. Ubuntu 24.04 gives you 5.020, which is fine.

If it says 4.something, you're on Ubuntu 22.04, and Block 2's commands won't work. On
Windows, go back to Part 0 and install Ubuntu 24.04. On a Linux laptop, talk to a lead.

---

## Part D: LibreLane (Block 3)

LibreLane is the set of tools that turns a design into a chip layout. It's a large
download (several GB), so start it when you have good Wi-Fi and some time. We install it
with a tool called Nix, which makes sure everyone gets exactly the same versions.

### D1. Install Nix

This is the command LibreLane's own documentation gives. It also points Nix at a server
that has everything prebuilt. Without that part, Nix would try to build every tool from
scratch, which takes hours. Copy the whole box as one paste, all five lines:

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://artifacts.nixos.org/nix-installer | sh -s -- install --no-confirm --extra-conf "
    extra-substituters = https://nix-cache.fossi-foundation.org
    extra-trusted-public-keys = nix-cache.fossi-foundation.org:3+K59iFwXqKsL7BNu6Guy0v+uTlwsxYQxjspXzqLYQs=
    extra-experimental-features = nix-command flakes
"
```

Enter your password if it asks. It takes about 5 minutes. When it finishes, **close the
terminal and open a new one**, then check:

```bash
nix --version
```

### D2. Download the ASIC LibreLane tutorial

```bash
cd ~
git clone https://github.com/bdawgcodes28/Su26LLEX.git
```

### D3. Start the LibreLane environment once

```bash
nix-shell ~/Su26LLEX/shell.nix
```

The first time, this downloads the whole toolchain. Expect 10 to 40 minutes depending on
your internet. When it's done, your prompt changes to start with `[nix-shell`. Check that
LibreLane is there:

```bash
librelane --version
```

Type `exit` to leave the environment. You'll come back to it in Block 3, and it starts in
seconds after the first time.

> **Why is there a `librelane` folder inside `Su26LLEX`?** Su26LLEX is a copy of LibreLane
> with a tutorial added on top, so the folder inside it is expected. Paths in the tutorial
> like `librelane/examples/...` are correct.

**If Nix fails, or your laptop doesn't have the space,** tell a lead before Block 3 starts
so there's time to work out another option.

---

## Part E: A text editor

Use whatever you like. If you don't have a favorite, install
[VS Code](https://code.visualstudio.com/) and add these extensions from the Extensions tab
on the left:

- **WSL** (Windows only). It lets VS Code open files inside Ubuntu. From the Ubuntu window,
  `cd` into a folder and type `code .` to open it.
- **Verilog-HDL/SystemVerilog** by mshr-h, for syntax colors in `.v` and `.sv` files.

---

## Check everything at once

From inside the repo folder, run:

```bash
cd ~/silicon-aggies-onboarding
bash setup/check.sh
```

It prints `ok` or `MISSING` for each tool. If anything says `MISSING`, paste that output in
the GroupMe or bring it to the help session.
