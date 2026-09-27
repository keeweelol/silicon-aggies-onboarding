# Block 3: Physical Design (from code to layout)

**Two weeks, Oct 19 to Oct 30.**

So far your designs have been text. In this block you turn text into geometry: the actual
rectangles of metal and silicon, at exact positions, that a factory can build. You run the
ASIC LibreLane tutorial once to learn the tools, then do the same thing to the counter-SRAM
you fixed in Block 2.

---

## What you'll make

A `.gds` file of your counter-SRAM. GDS is the file format chip factories accept, and it's
the same format we submit to Tiny Tapeout. You'll open it in a layout viewer called KLayout,
take screenshots, and read the reports the tools produce.

This block also feels different from the first two. You write almost no code. Instead you
set up a config file, run a long tool flow, and read what the tools tell you. Some people
love that and some don't, and both are useful to find out before you pick a team.

## What you need to know going in

- **Block 2.** You need your fixed `counter_sram.sv`. If you didn't finish Block 2, ask a
  lead for help getting a working copy.
- **Nothing about chip layout.** Lesson 0 explains every step in plain language.

## How the two weeks run

| When | What |
|---|---|
| Before Oct 19 | Make sure LibreLane is installed (setup Part D). If it won't install, ask a lead for a lab machine **now**. |
| Monday, week 1 | 30-minute kickoff. A lead starts a run and shows a finished layout. |
| Week 1 | Lessons 0, 1, and 2: learn the stages, run the tutorial, run your design. |
| Middle weekend | Open lab. Leads are in the room. |
| Week 2 | Lessons 3 to 6: read the reports, look at the layout, change one setting, turn it in. |
| Friday, Oct 30, 11:59 PM | Pull request due. |

## The lessons

| # | Lesson | About how long |
|---|---|---|
| 0 | [What "hardening" means](lessons/00-what-hardening-means.md): the six stages | 20 min |
| 1 | [Run the tutorial](lessons/01-run-the-tutorial.md): prove your tools work | 1 hr (mostly waiting) |
| 2 | [Harden your design](lessons/02-harden-your-design.md): run the flow on your counter-SRAM | 45 min |
| 3 | [Read the reports](lessons/03-read-the-reports.md): find the numbers that matter | 45 min |
| 4 | [Look at the layout](lessons/04-look-at-the-layout.md): KLayout and screenshots | 30 min |
| 5 | [Change one thing](lessons/05-change-one-thing.md): see what a setting does | 45 min |
| 6 | [Turn in your work](lessons/06-submit.md): write-up and pull request | 45 min |

Keep these open while you work:

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): errors you're likely to hit, with fixes.
- [GLOSSARY.md](GLOSSARY.md): every new term in this block.

## Before you start

You need LibreLane from Part D of the [setup guide](../setup/README.md). Check it:

```bash
nix --version
ls ~/Su26LLEX
```

If `nix` isn't found, or the `Su26LLEX` folder doesn't exist, go back to setup Part D.
This block is mostly about getting the tools to run, so get that sorted before Oct 19. If
Nix won't install on your laptop, tell a lead so they can reserve you a lab machine.

> **Windows 10:** KLayout needs to open a window, and WSL on Windows 10 can't do that
> without extra setup. Plan to do Lesson 4 on a lab machine or a friend's Windows 11 or Mac
> laptop.

## What you turn in

In `submissions/physical-design/YOUR-GITHUB-USERNAME/`:

- [ ] `src/counter_sram.sv`: the design you hardened
- [ ] `config.yaml`: your config, including the change from Lesson 5
- [ ] `counter_sram.gds`: the final layout
- [ ] `layout.png`: KLayout screenshot of the whole chip
- [ ] `layout-zoom.png`: KLayout screenshot zoomed in far enough to see single cells
- [ ] `metrics.md`: the filled-in metrics table, for both runs
- [ ] `WRITEUP.md`: 300 to 500 words
- [ ] a pull request, opened by Friday Oct 30

**Don't turn in the `runs/` folder.** It's hundreds of megabytes. Lesson 6 shows you how to
copy out only the file you need.

## When you're done

A lead merges your pull request when:

- the flow finished all the way through signoff, with zero DRC errors and a clean LVS
  result (Lesson 3 explains these),
- worst slack (WNS) is zero or positive at your clock period,
- both screenshots are readable, and
- your write-up explains all six stages in your own words, using numbers from your own run.

## Getting help

Post in the ASIC GroupMe with the command you ran, the full error text (copy and paste it),
and your operating system. For flow errors, also post the name of the step that failed.
It's in the last few lines of the output.

Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first.
