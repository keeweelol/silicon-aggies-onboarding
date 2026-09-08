# Lesson 1 — Your first simulation

Goal: run a design that already works, see its output, and open a waveform. You write no
code in this lesson.

The point is to confirm your tools work **now**, while there's no deadline pressure. If
something is broken, today is a great day to find out.

---

## Step 1 — Get your folder set up

```bash
cd ~/silicon-aggies-onboarding
mkdir -p submissions/digital-design/YOUR-GITHUB-USERNAME
cd submissions/digital-design/YOUR-GITHUB-USERNAME
cp ../../../digital-design/starter/* .
ls
```

You should see: `Makefile`, `check.py`, `blinker.v`, `tb_blinker.v`,
`tt_um_traffic_light.v`, `tb_traffic_light.v`.

Everything you do for this block happens in this folder.

## Step 2 — Run the blinker

```bash
make warmup
```

You should get:

```
tick   led
----------
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

**That's a simulation.** You just ran a piece of hardware that doesn't exist, on a clock
that doesn't exist, and watched an LED that doesn't exist turn on. The LED flips every 8
ticks.

If this failed, stop here and check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md). Do not
move on with broken tools.

## Step 3 — Read the design

Open `blinker.v`. It's about fifteen lines. Here's the part that matters:

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

Everything from Lesson 0 is here: an `always @(posedge clk)` block, an active-low reset,
`<=` for the assignments, and an `assign` connecting an internal `reg` out to a pin.

**A question worth sitting with for a second:** `counter` is 3 bits wide. Three bits can
hold 0 through 7. So what happens on the tick after it reaches 7? Nothing in the code
says to wrap it back to 0.

It wraps anyway — 7 + 1 in three bits is 0, the same way an odometer rolls over. That's
not a Verilog rule, it's how binary addition works in fixed-width hardware. **You will use
this constantly**, and it's also a place bugs hide when you didn't intend it.

## Step 4 — Open the waveform

The simulation wrote a file called `blinker.vcd`. That's a recording of every signal at
every moment. Open it:

```bash
gtkwave blinker.vcd &
```

The `&` puts it in the background so you get your terminal back.

**GTKWave is ugly and unintuitive. Here's the ten percent you need:**

1. Top-left panel lists the modules. Click **`tb_blinker`**, then **`dut`**.
2. The panel below fills with signal names.
3. Click `clk`, then ctrl-click `rst_n`, `counter`, and `led`.
4. Click the **Append** button (or drag them into the big black area).
5. Press **Shift+Alt+F** to zoom to fit, or click the magnifier-with-a-square icon.

You should now see waves. `clk` ticking, `counter` climbing 0→7 and rolling over, `led`
flipping every eighth tick.

**Zoom in** until you can see individual clock edges. Notice that `counter` changes right
at the rising edge of `clk`, never in between. That's what `always @(posedge clk)` means,
drawn as a picture.

> **Can't open GTKWave?** On Windows 10 without an X server it won't launch. Use
> [Surfer](https://surfer-project.org/) in your browser instead — upload the `.vcd` file,
> no install. Same information.

## Step 5 — Break it on purpose

This is the most useful thing you'll do today.

Open `blinker.v` and change `if (counter == 3'd7)` to `if (counter == 3'd3)`. Save, then:

```bash
make warmup
```

The LED now flips every 4 ticks instead of 8. Look at the waveform again and confirm the
picture changed the way you expected.

**Now put it back to `3'd7`.** Then try one more: change `led <= ~led;` to `led <= 1'b1;`
and predict what happens *before* you run it. Were you right?

That loop — change something, predict the result, run it, check — is the entire job. Not
just this block. The job.

---

## What you should have now

- Your tools work.
- You've seen a simulation print output.
- You've opened GTKWave and gotten signals onto the screen.
- You've changed a design and watched the waveform change.

If any of those is false, sort it out before Lesson 3. Post in `#help` or bring it to
open lab.

---

**Next:** [Lesson 2 — State machines](02-state-machines.md). The one idea the project is
built on.
