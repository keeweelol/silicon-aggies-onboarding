# Lesson 2 — State machines

One idea, and then you draw your design on paper before writing any code.

---

## The idea

A **state machine** is hardware that is always in exactly one of a small number of
situations, and moves between them based on what happens.

You already know a dozen of them. A microwave is off, cooking, or paused. A vending
machine is waiting for money, has partial payment, or is dispensing. A traffic light is
green, yellow, or red.

Three pieces, and that's the whole concept:

- **States** — the situations it can be in. Exactly one at a time.
- **Transitions** — what causes it to move from one state to another.
- **Outputs** — what it does while it's in each state.

## Why this matters for hardware

A state machine is a **register that holds which state you're in**, plus logic that
decides the next state, plus logic that drives the outputs. That's it. That's the shape
of nearly every control circuit ever built, including the ones inside the chip we're
taping out.

In Verilog:

```verilog
localparam S_GREEN  = 2'b00;      // name the states
localparam S_YELLOW = 2'b01;
localparam S_RED    = 2'b10;

reg [1:0] state;                  // the register that remembers which one we're in

always @(posedge clk) begin
    if (!rst_n) begin
        state <= S_RED;           // reset always lands in a known state
    end else begin
        case (state)
            S_GREEN:  if (something) state <= S_YELLOW;
            S_YELLOW: if (something) state <= S_RED;
            S_RED:    if (something) state <= S_GREEN;
            default:                 state <= S_RED;
        endcase
    end
end

assign uo_out[2] = (state == S_GREEN);   // outputs come FROM the state
```

Notice the last line. **The outputs are derived from the state, not stored separately.**
That's important — if you keep a separate `green` register and update it by hand in each
branch, you'll eventually forget one and get two lights on at once.

## The timer

Traffic lights don't change on an event, they change after a *duration*. So you need a
counter running alongside the state:

```verilog
reg [4:0] timer;
```

The pattern is: every tick, either the timer goes up, or you change state and reset the
timer to zero.

```verilog
S_YELLOW: begin
    if (timer == YELLOW_TIME - 1) begin
        state <= S_RED;
        timer <= 5'd0;          // reset the timer on the way out
    end else begin
        timer <= timer + 5'd1;
    end
end
```

**Every path that changes state must also clear the timer.** Miss one and you get a light
that behaves fine for one cycle and then goes haywire. This is the single most common bug
in this project.

Why `YELLOW_TIME - 1`? Because the timer starts at 0. Counting 0,1,2,3 is four ticks. If
you compare against `YELLOW_TIME` you'll get five. Off-by-one errors here are normal and
the waveform will show you immediately.

## Remembering something that only happens for an instant

Here's the part of the project that requires actual thought.

The pedestrian button is a **single-cycle pulse**. Somebody presses it, it's high for one
tick, and then it's gone. It might arrive during yellow, or during red, or in the first
tick of green.

So this does not work:

```verilog
S_GREEN: begin
    if (ped_button) ...      // WRONG
end
```

By the time you're ready to act on it, the pulse is long over. You'd only catch a press
in the exact tick you happened to be looking.

You need to **remember** it:

```verilog
reg ped_req;                       // "somebody pressed, and we owe them a walk"

always @(posedge clk) begin
    if (ped_button) ped_req <= 1'b1;    // catch it whenever it arrives
    // ... and clear it somewhere, once you've honored it
end
```

Now the FSM tests `ped_req`, which stays high until you clear it, instead of `ped_button`,
which is gone in a flash.

**This is the actual lesson of the project.** Catching a brief event and holding it until
you can deal with it is something you'll do in nearly every design you ever build. It has
a name — request latching — and now you've done it once.

The remaining question is *where* to clear it, and that one is yours to work out.

---

## Now draw yours

Get paper. Actual paper.

Draw three circles: GREEN, YELLOW, RED. Draw arrows between them. On each arrow, write the
condition that causes that transition. Inside each circle, write which outputs are on.

Then answer these on the drawing, in writing:

1. **What makes GREEN → YELLOW happen?** There are two separate reasons. Write both.
2. **Where does `ped_req` get cleared?** Mark the exact spot.
3. **Which state does reset land in?**
4. **What is `walk` doing in each state?**

Take a photo of it and save it as `state-diagram.jpg` in your submission folder. **This is
a required deliverable** — leads read it first when reviewing.

It feels like a formality. It isn't. Everybody who skips this and goes straight to typing
writes their state machine twice. Ten minutes with a pen saves an hour with a keyboard.

---

**Next:** [Lesson 3 — Build the traffic light](03-build-it.md). Now you write code.
