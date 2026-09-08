# Block 1 — Digital Design: Traffic Light Controller

**Two weeks. Sep 21 – Oct 2.**

You are going to describe a traffic light in a hardware language, simulate it, and watch
it run. No prior Verilog required. If you have taken digital logic, you have everything
you need.

---

## What you'll build

A traffic light that cycles green → yellow → red on a timer, with a pedestrian button
that interrupts the cycle. Push the button during green and the light goes yellow early
so people can cross — but not *so* early that cars get a one-second green.

That's it. It sounds small, and it is. It's also a real finite state machine with a
timer and an asynchronous external event, which is the same shape as the control logic
in the chip we tape out in the spring.

## What you need to know going in

**Nothing about Verilog.** Lesson 0 teaches you the five things you need. Most people get
through it in half an hour.

**One thing about digital logic:** you should know what a flip-flop is and roughly what
"on the rising edge of the clock" means. If that's fuzzy, say so in `#help` — it's a
ten-minute conversation, not a semester of catching up.

## How the two weeks run

There is no lecture. There's a demo, an open lab, and this repo.

| When | What |
|---|---|
| **Monday, week 1** | 30-minute kickoff. A lead builds a small design live, start to finish. Come to this. |
| **Week 1** | Lessons 0 through 2. Get the tools running, simulate something that already works, learn state machines. |
| **Middle weekend** | Open lab. Leads in the room. Bring your laptop and whatever is broken. |
| **Week 2** | Lesson 3 — build the traffic light. Lesson 4 — submit it. |
| **Friday, Oct 2, 11:59 PM** | Pull request due. |

You can absolutely finish faster than this. The schedule is the slow path, not the target.

## The lessons

Work through these in order. Don't skip to Lesson 3 — Lesson 1 is where you find out
whether your tools actually work, and finding that out on the last day is bad.

| | Lesson | Time |
|---|---|---|
| 0 | [Verilog in 30 minutes](lessons/00-verilog-primer.md) — the five things you need | 30 min |
| 1 | [Your first simulation](lessons/01-first-simulation.md) — run a blinker, read a waveform | 30 min |
| 2 | [State machines](lessons/02-state-machines.md) — the idea, and drawing yours | 45 min |
| 3 | [Build the traffic light](lessons/03-build-it.md) — the actual project | a few hours |
| 4 | [Submit your work](lessons/04-submit.md) — git, pull request, done | 20 min |

Also here when you need them:

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — every error we expect you to hit, and the fix. Check this before posting in `#help`.
- **[GLOSSARY.md](GLOSSARY.md)** — every term in these lessons, in plain language.

## Before you start

Install the tools: [`../setup/README.md`](../setup/README.md). You need `iverilog`,
`gtkwave`, `git`, and `python3`. On Windows that means WSL2, and everything happens inside
Ubuntu.

Check it worked:

```bash
iverilog -V
gtkwave --version
```

If either says "command not found," go back to setup. Don't start Lesson 1 with broken
tools.

## What you turn in

Five things, in `submissions/digital-design/YOUR-GITHUB-USERNAME/`:

- [ ] `tt_um_traffic_light.v` — your design
- [ ] `state-diagram.jpg` — a photo of the diagram you drew on paper
- [ ] `waveform.png` — a screenshot from GTKWave
- [ ] `WRITEUP.md` — 300–500 words, template provided
- [ ] A pull request, opened by Friday Oct 2

**You can check your own work before submitting.** Run `make check` and it tells you
exactly what's missing or broken — the same things a lead looks at. Get it to say
`READY TO SUBMIT` and you're done.

## How this is graded

It isn't, really. Every submission is pass or another-pass. There is no curve, no ranking,
and nobody is comparing your design to anyone else's.

What we're actually looking at is whether you finished, and whether the write-up sounds
like you understood what you built. Somebody who finishes three of these on time over six
weeks is going to be a useful member. Somebody who doesn't, won't — no matter how much
Verilog they already knew walking in.

## Getting help

Post in `#help` with three things: **what you ran**, **the full error text** (copy-paste,
not a photo), and **your OS**. Leads answer in public so the next person with the same
problem finds the answer.

Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first. There's a good chance your error is
already in there with a fix.

There is no such thing as a question that's too basic here. Most of us learned this stuff
six months ago.
