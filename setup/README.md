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
  done when you see the prompt again. That's the line ending in `$` on Ubuntu, or `%` on a
  Mac.
- To paste in the Ubuntu window, right-click or press Ctrl+Shift+V. Plain Ctrl+V often
  doesn't work there. On a Mac, Cmd+V works.
- Anything after a `#` in a command box is a note for you to read. You can paste it along
  with the command. The terminal ignores it.
- Some boxes have a line for each kind of computer, marked `# Mac` or
  `# Ubuntu / Windows`. Run **only the line for yours**. The other one will just say
  `command not found`.
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

`~` is short for your home folder. On Ubuntu it's `/home/yourname`, and on a Mac it's
`/Users/yourname`.

Three shortcuts that save a lot of typing:

| Key | What it does |
|---|---|
| Up arrow | Brings back the last command you ran, so you can run it again |
| Tab | Finishes a file or folder name for you. Type `cd sil` and press Tab |
| Ctrl+C | Stops a command that's stuck or taking forever (Ctrl+C on a Mac too, not Cmd+C) |

### Using the terminal inside VS Code

If you'd rather stay in VS Code, it has a terminal built in, and every command in this repo
works there the same way.

1. **Open the repo folder, not a single file.**
   - **Mac:** in VS Code, choose **File**, then **Open Folder**, and pick
     `silicon-aggies-onboarding` in your home folder.
   - **Windows:** open the Ubuntu window and run `cd ~/silicon-aggies-onboarding`, then
     `code .`. VS Code opens connected to Ubuntu. The bottom-left corner should say
     **WSL: Ubuntu-24.04**. If it doesn't, you opened the Windows copy of VS Code by itself,
     and the tools won't be found. Close it and open it again from the Ubuntu window.
2. **Open the terminal:** **Terminal**, then **New Terminal**. It appears at the bottom of
   the window, already inside the repo folder.
3. **Check that it's the right kind of terminal.** The prompt should end in `$` (Windows,
   through Ubuntu) or `%` (Mac). If it starts with `PS C:\`, that's PowerShell, and none of
   the commands here will work. On Windows, go back to step 1.

A few differences from a normal terminal window:

- Paste with Ctrl+V (Cmd+V on a Mac).
- If you paste several lines at once, VS Code asks whether you really want to. It's safer to
  paste one line at a time anyway.
- GTKWave and Surfer still open in their own windows, outside VS Code.
- The terminal's folder doesn't follow the file you have open. If you open a file in the
  sidebar, the terminal stays where it was. Check your prompt, and `cd` if you need to.

### If you get lost

Almost every confusing error comes from being in the wrong folder. `No such file or
directory`, `No rule to make target`, and a missing file are all usually this. Your prompt
shows the folder you're in, just before the `$` or `%`. If it's not the folder the lesson
expects, the lesson always gives you a `cd` command near the top to get back. Run that one,
then try again.

If that doesn't fix it, post in the GroupMe with the command you ran and everything it
printed. Copy and paste the text instead of sending a photo.

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


### Surfer quick guide (Mac)

The lessons give GTKWave steps. Here's how to do the same things in Surfer:

| To do this | In Surfer |
|---|---|
| Open a waveform | `surfer dump.vcd &` (or whatever the `.vcd` file is called) |
| Add signals | In the left sidebar, click the testbench (`tb_blinker`, `tb_traffic_light`, or `test`), and `dut` under it if the lesson says so. Its signals are listed below. Click a signal name to add it, or drag it into the waveform area. |
| Zoom so everything fits | **View**, then **Zoom to fit**, or the zoom-to-fit button in the toolbar |
| Show a number in decimal | Right-click the signal's name next to the waveform, choose **Format**, then **Unsigned** |
| Reload after you rerun the simulation | Press `r`, or **File**, then **Reload**. Surfer may also offer to reload on its own when the file changes. |

**Screenshots on a Mac.** Press Cmd+Shift+4 and drag a box. The picture lands on your Desktop
with a long name like `Screenshot 2026-10-12 at 9.41.12 PM.png`. Move it into the folder
you're in and rename it in one step, using the file name the lesson asks for:

```bash
mv ~/Desktop/Screenshot*.png waveform.png
```

Do this right after each screenshot, while it's the only one on your Desktop.

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

You can run every command in this repo from VS Code's built-in terminal instead of a
separate window. See [Using the terminal inside VS Code](#using-the-terminal-inside-vs-code).

---

## Check everything at once

From inside the repo folder, run:

```bash
cd ~/silicon-aggies-onboarding
bash setup/check.sh
```

It prints `ok` or `MISSING` for each tool. If anything says `MISSING`, paste that output in
the GroupMe or bring it to the help session.
