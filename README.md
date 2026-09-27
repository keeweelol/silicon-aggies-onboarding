# ASIC onboarding, Fall 2026

Welcome to ASIC (Aggie Silicon & Integrated Circuits). This repo has everything you need
for your first six weeks in the org.

You don't need any chip design experience to start. If you've taken a digital logic class,
or you're taking one now, you know enough. Every guide in here assumes you've never used
these tools before and walks you through them one command at a time.

---

## Start here

Do these in order.

1. **Set up your computer.** Follow [`setup/README.md`](setup/README.md). It takes about an
   hour and a half. Everything after this depends on it, so do it first.
2. **Block 1: Digital Design.** Build a traffic light controller.
   Start at [`digital-design/README.md`](digital-design/README.md).
3. **Block 2: Verification.** Write testbenches and hunt down planted bugs.
   Start at [`verification/README.md`](verification/README.md).
4. **Block 3: Physical Design.** Turn your design into a real chip layout.
   Start at [`physical-design/README.md`](physical-design/README.md).
5. **Pick your team.** After Block 3 you choose the team you want to join.

Each block has a README that tells you what you're building and links to short lessons.
Work through the lessons in order. Each one ends with a link to the next.

---

## What the six weeks look like

Everyone in the new cohort moves through the same block at the same time. Each block is
two weeks long and has one small project.

| Block | Dates | What you make | Tools you learn |
|---|---|---|---|
| 1. Digital Design | Sep 21 to Oct 2 | A traffic light controller written in Verilog | Icarus Verilog, GTKWave |
| 2. Verification | Oct 5 to Oct 16 | Testbenches that find bugs in a counter and a small memory | Verilator, GTKWave |
| 3. Physical Design | Oct 19 to Oct 30 | A chip layout of the design you fixed in Block 2 | LibreLane, KLayout |

Every block runs on the same rhythm:

- **Monday of week 1:** a 30-minute kickoff where a lead does the project live. Come to this.
  It's the easiest way to see what you're aiming for.
- **The weekend in the middle:** an open lab. Leads are in the room. Bring your laptop and
  whatever is broken.
- **Friday of week 2, 11:59 PM:** your pull request is due.

Between those, you work on your own time from the guides in this repo. You can finish
faster than the schedule. The dates are the slowest you should go, not a pace you have
to match.

## Calendar

| Date | Event |
|---|---|
| Sep 8 (Tue) | IEEE Student Branch first GBM, recruiting pitch |
| Sep 17 (Thu) | ASIC interest meeting and toolchain install night |
| Sep 21 to Oct 2 | **Block 1: Digital Design** |
| Oct 5 to Oct 16 | **Block 2: Verification** |
| Oct 19 to Oct 30 | **Block 3: Physical Design** |
| Week of Nov 2 | Team placement. You choose, leads confirm |
| Nov 2 to Nov 18 | MAC tile design and hardening |
| Nov 18 | Last day to submit for the internal competition |
| Around Nov 20 | Internal competition, judged by Dr. Limbrick and an Apple engineer |
| December 2026 | Tiny Tapeout TTSKY26d closes |
| June 2027 | Chips come back. Bring-up event |

---

## How you turn in work

You turn in every project as a pull request on GitHub. A pull request is a way of saying
"here are my files, please look at them." A lead reviews it and either accepts it or leaves
comments asking for changes.

The first time takes about 20 minutes, and Block 1's
[Lesson 4](digital-design/lessons/04-submit.md) walks you through every click. The short
version:

1. Fork this repo on GitHub, once, at the start of the semester. (Setup covers this.)
2. Put your work in `submissions/<block-name>/<your-github-username>/`.
3. Make a branch, commit, push, and open a pull request.

We do it this way on purpose. Opening a clean pull request is a skill every engineering job
expects, and by November you'll have public commits on a chip design project.

## How it's graded

It isn't, really. Every submission is either "done" or "needs another pass." There's no
curve and no ranking.

A block is done when a lead merges your pull request. That happens when:

- every file on that block's deliverables list is there,
- a lead can run your work and get the same result you did, and
- your write-up is in your own words.

Late is fine if you tell a lead before the deadline. What we worry about is people who go
quiet. If you get stuck in week one and disappear, we can't help you.

## Getting help

Post in the ASIC GroupMe. Include three things:

1. the command you ran,
2. the full error message (copy and paste the text, don't send a photo of your screen),
3. your operating system (Windows, Mac, or Linux).

Before you post, check the troubleshooting page for your block. Your error is probably
already there with a fix.

No question is too basic. Most of the leads learned this stuff less than a year ago and hit
the same errors you will.

---

## What's in this repo

```
silicon-aggies-onboarding/
├── README.md             you are here
├── setup/                install the tools (do this first)
├── digital-design/       Block 1: traffic light controller
├── verification/         Block 2: find the bug
├── physical-design/      Block 3: design to layout
├── submissions/          where your work goes, one folder per person
└── LEADS.md              how leads run the program (you don't need this)
```
