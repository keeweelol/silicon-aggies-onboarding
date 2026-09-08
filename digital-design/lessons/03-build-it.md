# Lesson 3 — Build the traffic light

This is the project. Everything before now was preparation.

---

## The spec

Read this carefully. Every sentence is something the tests check.

**Normal cycle**, measured in clock ticks:

```
GREEN (12) → YELLOW (4) → RED (10) → GREEN → ...
```

**Reset.** `rst_n` is active low and synchronous. On reset the light goes to RED, the
timer clears, and the pedestrian request clears.

**Walk.** The `walk` output is high for the whole RED state, whether or not anyone
pressed the button.

**One-hot outputs.** Exactly one of red/yellow/green is on at any tick. Never zero, never
two.

**The pedestrian button** is a single-cycle pulse on `ui_in[0]`, and it can arrive at any
time:

- Press during GREEN, at or after tick `MIN_GREEN` (4): cut green short, go to YELLOW.
- Press during GREEN before tick 4: **remember it**, and act on it the moment tick 4
  arrives. Cars never get a green shorter than 4 ticks.
- Press during YELLOW or RED: nothing happens. Walk is already coming.
- The request clears while the light is RED, so a press during red doesn't carry over and
  shorten the next green.

## Pin map

```
ui_in[0]     pedestrian button
ui_in[7:1]   unused

uo_out[0]    car_red
uo_out[1]    car_yellow
uo_out[2]    car_green
uo_out[3]    walk
uo_out[7:4]  unused, drive 0

uio_*        unused this block, tie to 0
clk, rst_n, ena   standard
```

This is the real Tiny Tapeout pin contract. You're using it in week one so it's familiar
by the time we tape out.

---

## The starter file

Open `tt_um_traffic_light.v`. You already have it in your folder. It gives you the port
list, the timing constants, the state names, and the registers. There are four TODOs.

```verilog
    localparam GREEN_TIME  = 12;
    localparam YELLOW_TIME = 4;
    localparam RED_TIME    = 10;
    localparam MIN_GREEN   = 4;

    localparam S_GREEN  = 2'b00;
    localparam S_YELLOW = 2'b01;
    localparam S_RED    = 2'b10;

    wire ped_button = ui_in[0];

    reg [1:0] state;
    reg [4:0] timer;
    reg       ped_req;
```

**TODO 1** — reset. `state <= S_RED`, `timer <= 0`, `ped_req <= 0`.

**TODO 2** — latch the pedestrian request. Set `ped_req` when the button pulses, clear it
while RED.

**TODO 3** — the state machine and the timer. One `case` on `state`. Each tick, either
increment the timer, or change state and clear the timer to 0. Include a `default` that
sends you back to RED.

**TODO 4** — drive the outputs from `state`.

You write it all in **one** `always @(posedge clk)` block. Use `<=`.

---

## The build loop

Don't write all four TODOs and then run it. Write a piece, run it, look. Here's a
sensible order.

### Round 1 — get out of the dark

Do TODO 1 and TODO 4 only. Skip the state machine entirely. Reset the state to RED and
drive the outputs from it.

```bash
make
```

Test 1 should pass — the light is red after reset and walk is on. Everything else fails.
That's fine. **You now have a light that turns on**, which is much more progress than it
sounds.

### Round 2 — make it cycle

Add TODO 3, but only the plain timing. Forget the button completely for now:

- GREEN → YELLOW when `timer == GREEN_TIME - 1`
- YELLOW → RED when `timer == YELLOW_TIME - 1`
- RED → GREEN when `timer == RED_TIME - 1`

Run it. Test 2 should now pass — 12, 4, 10.

If your numbers are off by one, that's the `- 1`. If the light flickers between two
states, you forgot to clear the timer on one of the transitions.

### Round 3 — the button

Add TODO 2, and add the extra exit condition to GREEN.

Green now leaves for yellow when **either** the timer expires **or** `ped_req` is set and
`timer >= MIN_GREEN - 1`.

Run it. Tests 3, 4, and 5 should pass.

If test 4 fails and says green lasted 12 ticks when it should have lasted 4, your press
is being forgotten — go back to Lesson 2 and look at the latching section again. That's
the whole point of the exercise, so it's worth working out rather than being told.

### Round 4 — all ten

```bash
make
```

You want:

```
  ALL 10 CHECKS PASSED
```

---

## When a test fails, look at the waveform

The tests tell you *what* is wrong. The waveform tells you *why*.

```bash
make wave
```

Add `clk`, `rst_n`, `ui_in[0]`, `state`, `timer`, and `uo_out[3:0]`. Find the moment the
test complained about and look at what `state` and `timer` are doing right there.

Nine times in ten the bug is visible in three seconds once you're looking at the right
tick.

---

## Take your screenshot

Once all ten pass, you still need `waveform.png`.

Get a view showing at least one full cycle and one pedestrian interrupt, with `state`,
`timer`, and the four outputs visible. Crop it so the signal names are readable. Save it
in your submission folder.

---

## Write it up

Copy the template:

```bash
cp ../../../digital-design/submission-template/WRITEUP.md .
```

300–500 words, in your own words. The questions are in the template. The one that matters
most is **"what broke and how did you figure out what was wrong."**

Answer that one honestly and specifically. "Nothing broke" isn't a strong answer, it's an
unexamined one — and being able to describe how you found a bug is more of what this club
is about than getting it right the first time.

---

## Check yourself before you submit

```bash
make check
```

This runs the same checks a lead runs: files present, design compiles, all ten behaviors
pass, write-up long enough and free of template placeholders.

Get it to say `READY TO SUBMIT`.

---

## If you finish early

Optional, no extra credit, but these are the natural next questions:

1. **Add a second road.** Two lights that must never both be green — the interlock problem
   in every real controller.
2. **Night mode** on `ui_in[1]`: red blinks, no cycling.
3. **Make the timing programmable** from `uio_in` instead of `localparam`s, then think
   about what that costs you in gates.

---

**Next:** [Lesson 4 — Submit your work](04-submit.md).
