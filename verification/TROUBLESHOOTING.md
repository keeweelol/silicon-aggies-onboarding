# Troubleshooting (Block 2)

Look for your error here before you ask in the GroupMe. It's probably below.

If it isn't, post the command you ran, the full error text (copy and paste it, don't send a
photo), and your operating system.

**Read only the first error.** Verilator messages start with `%Error` or `%Warning`, followed
by the file name, the line number, and the column: `t1.sv:4:38` means file `t1.sv`, line 4,
character 38. Go to that line, fix it, and run again. Later errors are often side effects of
the first.

---

## Setup problems

**`Invalid option: --binary`** or **`Invalid option: --timing`**
Your Verilator is version 4. You need 5.0 or newer. Run `verilator --version` to check, then
see Part C of the [setup guide](../setup/README.md).

**`g++: not found`**, **`make: not found`**, or **`c++: command not found`** while building
Verilator needs a C++ compiler to build your simulation. Run:
`sudo apt install -y build-essential`

**`verilator: command not found`**
It isn't installed, or you're in the wrong window. On Windows, use the Ubuntu window. See
setup Part C.

**GTKWave won't install or open on a Mac**
Use Surfer instead (`brew install surfer`), and type `surfer dump.vcd &` wherever a lesson
says `gtkwave dump.vcd &`.

**GTKWave won't open (Windows 10)**
Open `dump.vcd` in the [Surfer web viewer](https://surfer-project.org/) instead. It shows
the same waveform in your browser.

---

## Build errors (from the `verilator` command)

**`%Warning-IMPLICIT: ... Signal definition not found, creating implicitly: 'clk'`**
(usually followed by `Procedural assignment to wire` errors)
You haven't declared that signal yet. In your own testbench, that means Part 1 isn't filled
in, or a name is misspelled. Add `logic clk;` (and the other signals) near the top of the
module. The `Procedural assignment to wire` errors after it go away once the signal is
declared.

**`syntax error, unexpected logic, expecting ',' or ';'`**
The line *before* the one it points to is missing a semicolon. Every `logic ...` line ends
with `;`.

**`syntax error, unexpected '.', expecting ')'`**
A comma is missing between two port connections, like `.rst_n(rst_n) .en(en)`. It should be
`.rst_n(rst_n), .en(en)`.

**`Mixing positional and .*/named instantiation connection`**
There's an extra comma after the **last** port connection, like `.count(count),);`. Remove
the last comma.

**`Cell has missing pin: 'count'`**
Look at the **next** message before you do anything. This is the one time the first message
can mislead you.

- If the next line says **`Pin not found: 'cnt'`** (some other name in quotes), you didn't
  forget a port. You misspelled it. The name after the dot has to match the DUT's port name
  exactly, so `.cnt(count)` should be `.count(count)`. Check the `module` line of the
  design file.
- If there's no `Pin not found` line, you really did leave a port out. Add a connection for
  it.

**`%Warning-WIDTHTRUNC ... Exiting due to 1 warning(s)`**
Verilator stops on warnings. This one means you put a wider value into a narrower signal,
usually `write_data = i;` where `i` is 32 bits and `write_data` is 8. Use
`write_data = i[7:0];`.

**`Specified --top-module 'test' was not found in design`**
Your testbench module isn't named `test`, or you left the testbench file off the command.
The first line of the testbench should be `module test();`.

**`Cannot find file containing module: ...`**
One of two things. If the name in quotes ends in `.sv`, a file path in your command is
wrong: make sure you're in the right folder (run `pwd` and `ls`) and check the spelling. If
the name in quotes is a module name like `'counterx'`, the module name at the start of your
instance line is misspelled. It has to match the design's `module` line exactly (`counter`
or `counter_sram`).

---

## Run problems (from `./obj_dir/Vtest`)

**`No such file or directory: ./obj_dir/Vtest`**
The build failed, or you're in a different folder from where you built. Run the `verilator`
command again in this folder and check that it ends with `make: Leaving directory`.

**The simulation never ends**
Your test steps are missing `$finish;` at the end, or it's somewhere the code never reaches.
Press Ctrl+C to stop it.

**No `dump.vcd` file appears**
Your testbench is missing `$dumpfile("dump.vcd");` and `$dumpvars(0, test);` at the start of
the `initial begin` block.

---

## Waveform problems

**I fixed the code but the waveform didn't change**
Two things have to happen. First rerun **all three commands**, starting with `verilator`.
(`./obj_dir/Vtest` runs the old program until you rebuild.) Then press Ctrl+Shift+R in
GTKWave to reload the file.

**GTKWave opens but the signal panel is empty**
Click `test` in the top-left panel first. The signals show up in the panel below it. Select
them and click **Append**.

**`count` shows letters like A, B, F**
GTKWave shows numbers in hexadecimal by default. Right-click the signal, choose
**Data Format**, then **Decimal**.

**Everything looks off by one clock**
You're changing inputs right on the rising edge. Change them after `@(negedge clk);`
instead. See "Change inputs on the falling edge" in [Lesson 0](lessons/00-testbench-primer.md).

**The inputs don't do what I meant**
Before blaming the design, check your testbench. Look at `rst_n`, `en`, and `write_en` in
the waveform and compare them to your test steps. A lot of "design bugs" turn out to be
testbench bugs.

---

## Git problems

**`git status` lists `obj_dir/` or `dump.vcd`**
Those are build outputs and shouldn't be committed. Your repo is probably missing the latest
`.gitignore`. Run `git pull upstream main` from `~/silicon-aggies-onboarding` and check again.

**`git pull upstream main` says `'upstream' does not appear to be a git repository`**
You skipped the end of setup step A6. Run
`git remote add upstream https://github.com/zjohnson2005/silicon-aggies-onboarding.git`
and try again.

**`git checkout main` says your local changes would be overwritten**
You have unsaved Block 1 changes. Ask in the GroupMe before you do anything else, so you
don't lose work.

For anything else about git, see the git section of
[Block 1's troubleshooting page](../digital-design/TROUBLESHOOTING.md#git-and-github).
