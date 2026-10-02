# Lesson 1: Your first simulation

**Goal:** run a design that already works, read what it prints, and open its waveform. You
don't write any code in this lesson.

The main point is to prove your tools work now, while there's no deadline pressure. If
something is broken, today is the best day to find out.

> **New to the terminal?** Read
> [How to use the terminal](../../setup/README.md#how-to-use-the-terminal-read-this-if-you-never-have)
> in the setup guide first. It's five minutes, and it covers almost everything that trips
> people up in this lesson.
>
> **Using VS Code?** You can run everything from its built-in terminal. Setup has
> [a short section on it](../../setup/README.md#using-the-terminal-inside-vs-code). On
> Windows, make sure VS Code is connected to Ubuntu first.

---

## Step 1: Set up your folder

Open your terminal (the Ubuntu window on Windows) and run these one at a time. Replace
`YOUR-GITHUB-USERNAME` with your GitHub username in both places.

```bash
cd ~/silicon-aggies-onboarding
mkdir -p submissions/digital-design/YOUR-GITHUB-USERNAME
cd submissions/digital-design/YOUR-GITHUB-USERNAME
cp ../../../digital-design/starter/* .
ls
```

What those do: go to the repo, make a folder with your name, move into it, copy the starter
files in, and list them.

`ls` should show six files: `Makefile`, `check.py`, `blinker.v`, `tb_blinker.v`,
`tt_um_traffic_light.v`, and `tb_traffic_light.v`.

You'll do everything for this block inside this folder. If you close the terminal and come
back later, `cd` into it again first:

```bash
cd ~/silicon-aggies-onboarding/submissions/digital-design/YOUR-GITHUB-USERNAME
```

## Step 2: Run the blinker

```bash
make warmup
```

You should see something like this:

```
VCD info: dumpfile blinker.vcd opened for output.
tick   led
==========
   0    0
   1    0
   2    0
   3    0
   4    0
   5    0
   6    0
   7    1
   8    1
   ...
```

That's a simulation. You just ran a piece of hardware that doesn't physically exist, and
watched its LED turn on. The LED flips every 8 ticks.

If you got an error instead, stop here and look it up in
[TROUBLESHOOTING.md](../TROUBLESHOOTING.md). Don't move on with broken tools.

## Step 3: Read the design

Open `blinker.v` in your editor (or run `nano blinker.v`). It's about fifteen lines. This is
the part that matters:

```verilog
reg [2:0] counter;
reg       led;

always @(posedge clk) begin
    if (!rst_n) begin
        counter <= 3'd0;
        led     <= 1'b0;
    end else begin
        counter <= counter + 3'd1;
        if (counter == 3'd7)
            led <= ~led;
    end
end

assign uo_out[0] = led;
```

Everything from Lesson 0 is in here: an `always @(posedge clk)` block, an active-low
reset, `<=` for every assignment, and an `assign` that connects an internal `reg` to an
output pin.

Here's a question to think about. `counter` is 3 bits wide, so it can hold 0 through 7.
What happens on the tick after it reaches 7? Nothing in the code says to go back to 0.

It goes back to 0 anyway. In 3 bits, 7 + 1 is 0, the same way a car's odometer rolls over.
That's just how fixed-width binary addition works in hardware. You'll rely on this all the
time, and it's also a place where bugs hide when you didn't mean for it to happen.

## Step 4: Open the waveform

The simulation also wrote a file called `blinker.vcd`. It's a recording of every signal at
every moment. You'll open it in a **waveform viewer**, a program that draws those
recordings as pictures. On Ubuntu and Windows the viewer is GTKWave. On a Mac it's Surfer.

### First, make sure you're in the right folder

The viewer can only open `blinker.vcd` if your terminal is in the folder where that file is.
Run:

```bash
ls
```

You should see `blinker.vcd` in the list. If you don't, you're in the wrong folder, or
`make warmup` didn't finish. Go back to your folder and run it again:

```bash
cd ~/silicon-aggies-onboarding/submissions/digital-design/YOUR-GITHUB-USERNAME
make warmup
ls
```

> **Where am I?** Your prompt shows the name of the folder you're in, just before the `%` or
> `$`. If it says `YOUR-GITHUB-USERNAME` (your actual username), you're in the right place.
> `pwd` prints the full path if you want to be sure.

### Then open it

Run **only the line for your computer**. Don't paste both.

On Ubuntu or Windows:

```bash
gtkwave blinker.vcd &
```

On a Mac:

```bash
surfer blinker.vcd &
```

A new window opens. The `&` at the end keeps your terminal free while the viewer is open.
The terminal may print something like `[1] 12345`. That's normal. Press Enter if you don't
see your prompt again.

If you get `command not found`, the viewer isn't installed. Go back to Part B of the
[setup guide](../../setup/README.md).

The window starts out empty. That's expected. You have to pick which signals to show.

### Show the signals in GTKWave (Ubuntu and Windows)

GTKWave isn't pretty, and it isn't obvious how to use it. Here's what you need:

1. In the top-left panel, click **`tb_blinker`**, then click **`dut`** under it.
2. The panel below it fills with signal names.
3. Click `clk`, then hold Ctrl and click `rst_n`, `counter`, and `led`.
4. Click the **Append** button at the bottom. (You can also drag the signals into the big
   black area.)
5. Press **Shift+Alt+F** to zoom so the whole simulation fits. The toolbar button that looks
   like a magnifying glass with a square does the same thing.

### Show the signals in Surfer (Mac)

1. The left side of the window has two lists. The top one, **Scopes**, shows the parts of
   your design. Click **`tb_blinker`**, then click **`dut`** under it. (If you don't see
   `dut`, click the small arrow next to `tb_blinker` to open it.)
2. The bottom list, **Variables**, fills with signal names.
3. Click `clk`, `rst_n`, `counter`, and `led`, one at a time. Each one appears in the big
   area on the right as soon as you click it.
4. Open the **View** menu at the top and choose **Zoom to fit**, so the whole simulation
   fits on screen.

The [Surfer quick guide](../../setup/README.md#surfer-quick-guide-mac) has the rest of the
Surfer steps you'll need later, like reloading and showing numbers in decimal.

### What you should see

Now you should see the signals drawn as waves: `clk` ticking up and down, `counter` climbing
from 0 to 7 and rolling over, and `led` flipping every eighth tick.

Zoom in until you can see single clock edges. Notice that `counter` only changes exactly
when `clk` rises, never in between. That's what `always @(posedge clk)` means, drawn as a
picture.

> **GTKWave won't open?** On Windows 10 it can't open a window without extra setup. Use
> [Surfer](https://surfer-project.org/) in your browser instead. Open the site, load your
> `.vcd` file, and you'll see the same thing.

## Step 5: Break it on purpose

This is the most useful part of the lesson.

1. Open `blinker.v` and change `if (counter == 3'd7)` to `if (counter == 3'd3)`. Save the
   file.
2. **Before you run it,** write down your prediction. Will the LED flip faster, slower, or at
   the same speed?
3. Run `make warmup` again. In GTKWave, press **Ctrl+Shift+R** (in Surfer, press `r`) (or use File, then Reload
   Waveform) and check your prediction.
4. Most people predict "every 4 ticks," and most people are wrong. The LED still flips every
   8 ticks. It just flips at a different moment: the first flip now comes at tick 3 instead
   of tick 7. Look at `counter` in the waveform to see why. It still counts all the way up to
   7 and rolls over, so it only equals 3 once every 8 ticks. Changing the number you compare
   against moves *when* the LED flips, not *how often*. That's the rollover from Step 3 again.
5. To really make it flip every 4 ticks, compare only the bottom two bits of the counter,
   which roll over every 4 ticks: `if (counter[1:0] == 2'd3)`. Try it, then check the
   waveform.
6. Change it back to `if (counter == 3'd7)`.

Now try one more. Change `led <= ~led;` to `led <= 1'b1;`. **Before you run it,** write down
what you think will happen. Then run it and see if you were right. Change it back when
you're done.

Change something, predict what will happen, run it, check. You'll do that loop for the
rest of this block, and for the rest of any hardware job.

---

## Before you move on

You should be able to say yes to all of these:

- [ ] `make warmup` runs and prints the tick table.
- [ ] You opened GTKWave (or Surfer) and got signals on the screen.
- [ ] You changed the design and saw the waveform change.

If any of these isn't true yet, sort it out before Lesson 3. Ask in the GroupMe or bring
it to the help session.

---

**Next:** [Lesson 2: State machines](02-state-machines.md), the one idea the project is
built on.
