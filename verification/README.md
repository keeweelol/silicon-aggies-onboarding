# Block 2: Verification (find the bug)

**Two weeks, Oct 19 to Oct 30.**

In Block 1 we gave you a testbench that checked your design. In this block you learn to
write your own, and you use it to find bugs someone planted in a design on purpose.

The exercises in this block were written by Bryson Fields. His originals are in
[bdawgcodes28/Design-Verification-Exercises](https://github.com/bdawgcodes28/Design-Verification-Exercises).

---

## What you'll do

You work with two small designs:

1. a **4-bit counter**, which counts 0, 1, 2, ... up to 15 and then starts over, and
2. a **counter connected to a small memory** (an SRAM), where the counter picks which memory
   slot to read or write.

For each design, you first run a version that works, called the **golden** version. Then you
get a copy of the same design with bugs planted in it, called the **buggy** version. You
write or finish a testbench, look at the waveform, figure out what's wrong, and fix it.

Verification is its own job in industry, and on many chip teams verification engineers
outnumber designers. The reason is simple: once a chip is made, you can't patch it. The
fixed counter-SRAM you finish this block with is also the design you turn into a chip layout
in Block 3.

## What you need to know going in

- **Block 1.** You should be comfortable with `always @(posedge clk)`, `<=`, reading a
  waveform in GTKWave, and the terminal commands from setup.
- **No SystemVerilog.** The designs here are written in SystemVerilog, a newer version of
  Verilog. Lesson 0 covers the differences, and there aren't many.

## How the two weeks run

| When | What |
|---|---|
| Monday, week 1 | 30-minute kickoff. A lead runs the golden counter and the buggy counter side by side. |
| Week 1 | Lessons 0, 1, and 2: the counter. |
| Middle weekend | Online help session with the leads. |
| Week 2 | Lessons 3, 4, and 5: the counter-SRAM, then turn it in. |
| Friday, Oct 30, 11:59 PM | Pull request due. |

## The lessons

Do them in order. Each one ends with a link to the next.

| # | Lesson | About how long |
|---|---|---|
| 0 | [Testbenches in 30 minutes](lessons/00-testbench-primer.md): the SystemVerilog you need | 30 min |
| 1 | [Run the golden counter](lessons/01-golden-counter.md): the three commands you'll use all block | 45 min |
| 2 | [Find the bugs in the counter](lessons/02-buggy-counter.md): write your first testbench | 1 to 2 hrs |
| 3 | [Run the golden counter-SRAM](lessons/03-golden-counter-sram.md): how the memory works | 45 min |
| 4 | [Find the bugs in the counter-SRAM](lessons/04-buggy-counter-sram.md): finish a testbench, fix three bugs | 2 to 3 hrs |
| 5 | [Turn in your work](lessons/05-submit.md): write-up and pull request | 45 min |

Keep these open while you work:

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): errors you're likely to hit, with fixes.
- [GLOSSARY.md](GLOSSARY.md): every new term in this block, in plain language.

## Before you start

You need two tools from the [setup guide](../setup/README.md): Verilator (Part C) and
GTKWave (Part B). Check them:

```bash
verilator --version
gtkwave --version
```

Verilator must be **5.0 or newer**. If it says 4.something, see setup Part C before you do
anything else. None of the commands in this block work on Verilator 4.

## What's in this folder

```
verification/
├── README.md              you are here
├── lessons/               Lessons 0 to 5
├── golden_counter/        Lesson 1: the working counter and its testbench
├── buggy_counter/         Lesson 2: the counter with bugs, and a testbench outline you fill in
├── golden_counter_sram/   Lesson 3: the working counter-SRAM and its testbench
├── buggy_counter_sram/    Lesson 4: the counter-SRAM with bugs and a half-written testbench
└── submission-template/   the write-up you fill in for Lesson 5
```

## What you turn in

In `submissions/verification/YOUR-GITHUB-USERNAME/`:

- [ ] `buggy_counter/testbench/counter_tb.sv`: the testbench you wrote
- [ ] `buggy_counter/buggy_design/counter.sv`: the counter, with its bugs fixed
- [ ] `buggy_counter_sram/testbench/buggy_cosram_tb.sv`: the testbench, with both tasks done
- [ ] `buggy_counter_sram/buggy_design/counter_sram.sv`: the counter-SRAM, with its bugs fixed
- [ ] `waveform-counter.png`: GTKWave screenshot of your fixed counter
- [ ] `waveform-counter-sram.png`: GTKWave screenshot of your fixed counter-SRAM
- [ ] `WRITEUP.md`: your bug report
- [ ] a pull request, opened by Friday Oct 30

## When you're done

A lead merges your pull request when:

- both designs compile and run with the commands in the lessons, with no errors,
- your counter waveform shows all four counter spec lines, including counting past 15 and a
  reset in the middle of counting,
- your counter-SRAM waveform shows all five counter-SRAM spec lines,
- your testbenches show the bugs when you run them against the original buggy designs (the
  "prove it" step in Lessons 2 and 4), and
- your write-up points to the exact line that caused each bug.

## Getting help

Post in the ASIC GroupMe with the command you ran, the full error text (copy and paste it),
and your operating system. You can also email Bryson Fields (bafields1@aggies.ncat.edu) or
Zachary Johnson (zejohnson3@aggies.ncat.edu).

Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first. Your error is probably already there.
