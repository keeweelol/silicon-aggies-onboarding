# Block 1: Digital Design (traffic light controller)

**Two weeks, Oct 5 to Oct 16.**

You'll describe a traffic light in a hardware language called Verilog, run it in a
simulator, and watch it work. You don't need to know any Verilog yet. If you've taken
digital logic, you have what you need.

---

## What you'll build

A traffic light that goes green, then yellow, then red, on a timer. It also has a
pedestrian button. If someone presses the button while the light is green, the light turns
yellow early so they can cross. It won't turn *so* early that cars only get a one-second
green, though.

It's a small project, but it's a real finite state machine with a timer and an outside
event you have to react to. The control logic in the chip we tape out has the same shape.

## What you need to know going in

**No Verilog.** Lesson 0 teaches you the five ideas you need, and most people finish it in
half an hour.

**A little digital logic.** You should know what a flip-flop is and roughly what "on the
rising edge of the clock" means. If that's fuzzy, say so in the GroupMe. It's a ten-minute
conversation.

## How the two weeks run

There's no lecture. There's a demo, an open lab, and the lessons in this folder.

| When | What |
|---|---|
| Monday, week 1 | 30-minute kickoff. A lead builds a small design live. Come to this. |
| Week 1 | Lessons 0, 1, and 2. Get the tools working, run a design that already works, learn state machines. |
| Middle weekend | Open lab. Leads are in the room. Bring your laptop and whatever is broken. |
| Week 2 | Lesson 3 (build the traffic light) and Lesson 4 (turn it in). |
| Friday, Oct 16, 11:59 PM | Pull request due. |

You can finish faster than this. The schedule is the slowest you should go.

## The lessons

Do them in order. Don't jump to Lesson 3. Lesson 1 is where you find out whether your tools
work, and you want to find that out early, not the night before the deadline.

| # | Lesson | About how long |
|---|---|---|
| 0 | [Verilog in 30 minutes](lessons/00-verilog-primer.md): the five ideas you need | 30 min |
| 1 | [Your first simulation](lessons/01-first-simulation.md): run a blinker and read a waveform | 30 min |
| 2 | [State machines](lessons/02-state-machines.md): the idea, and drawing yours on paper | 45 min |
| 3 | [Build the traffic light](lessons/03-build-it.md): the project itself | a few hours |
| 4 | [Turn in your work](lessons/04-submit.md): git and the pull request | 20 min |

Keep these open while you work:

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) lists the errors we expect you to hit, with fixes.
  Check it before you ask in the GroupMe.
- [GLOSSARY.md](GLOSSARY.md) explains every term in these lessons in plain language.

## Before you start

Finish the [setup guide](../setup/README.md) first. For this block you need `git`,
`iverilog`, `gtkwave`, `python3`, and `make`. On Windows, everything happens inside the
Ubuntu window.

Check that the tools work:

```bash
iverilog -V | head -1
gtkwave --version
```

If either one says `command not found`, go back to setup. Don't start Lesson 1 with broken
tools.

## What you turn in

Five things, in `submissions/digital-design/YOUR-GITHUB-USERNAME/`:

- [ ] `tt_um_traffic_light.v`: your design
- [ ] `state-diagram.jpg`: a photo of the state diagram you drew on paper
- [ ] `waveform.png`: a screenshot from GTKWave
- [ ] `WRITEUP.md`: 300 to 500 words, using the template we give you
- [ ] a pull request, opened by Friday Oct 16

You can check your own work before you turn it in. Run `make check` in your folder. It
tells you what's missing or broken, which are the same things a lead checks. When it says
`READY TO SUBMIT`, you're done.

## How this is graded

Every submission is either "done" or "needs another pass." There's no curve and no
ranking, and nobody compares your design to anyone else's.

What we look at is whether you finished, and whether your write-up shows you understood
what you built.

## Getting help

Post in the ASIC GroupMe with three things: the command you ran, the full error text (copy
and paste it, don't send a photo), and your operating system. Leads answer in the group so
the next person with the same problem sees the fix too.

Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first. Your error is probably already there.

There's no such thing as a question that's too basic here. Most of us learned this stuff
within the last year.
