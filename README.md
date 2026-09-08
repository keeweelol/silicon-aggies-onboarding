# Silicon Aggies — Fall 2026 Rotation Program

Everything a new member needs to get through their first six weeks, and everything a
teaching lead needs to run them.

---

## 1. What the rotation is

Every new member rotates through all three technical areas — Digital Design,
Verification, and Physical Design — two weeks each, six weeks total. The entire cohort
moves through the same block at the same time. Members pick the team they want to join
at the *end* of the rotation, not the beginning.

Each block has one project. Each project has a written guide in this repo, a fixed list
of deliverables, and a definition of done. Finish three small projects on time and you
are a member in good standing with a team placement.

## 2. Why rotation instead of letting people pick

Silicon Jackets at Georgia Tech originally let members onboard directly into the subteam
they were most interested in, then changed to requiring exposure to all three. Their
reason: when students choose on prior familiarity alone, more than two thirds default to
digital design. That starves verification and physical design of people, and it leaves
members with no picture of how the flow fits together.

Rotation costs depth inside each block and buys two things — a better-informed placement
decision and a healthier distribution across teams. We are taking that trade.

There is an operational reason too. Running the whole cohort through the same material
at the same time means a tooling problem that hits fifty people gets solved once. Rolling
admission would force us to re-solve the same install problems all semester.

## 3. What onboarding is actually filtering for

Effort and follow-through, not existing skill.

The projects are deliberately reachable by someone who has taken digital logic and
nothing else. A member who finishes three small projects on time over six weeks will be
useful. A member who does not, will not, regardless of how much Verilog they already
know. Keeping the technical bar low and the completion bar firm is the entire point.

Nothing here is a competition and nothing is graded on a curve. Every deliverable is
pass / needs-another-pass.

## 4. Rotation order and why

**Block 1: Digital Design → Block 2: Verification → Block 3: Physical Design**

This is the order the work actually happens in industry: you describe hardware, you prove
it does what you claimed, then you turn it into geometry. It also lets each block feed
the next. The counter you verify in Block 2 is the counter you harden in Block 3, so
members are never handed a black box they have no relationship with.

> **Decision needed:** the original draft listed Physical Design second. Confirm the
> order above before September 12 — the guides cross-reference each other and the
> reordering is a five-minute edit now and an annoying one later.

## 5. Calendar

| Date | Event |
|---|---|
| Sep 8 (Tue) | IEEE Student Branch first GBM — recruiting pitch |
| Sep 12 (Sat) | **Internal deadline.** Repo, toolchain, and guides frozen |
| Sep 17 (Thu) | Silicon Aggies interest meeting + toolchain install night |
| Sep 21 – Oct 2 | **Rotation 1 — Digital Design** |
| Oct 5 – Oct 16 | **Rotation 2 — Verification** |
| Oct 19 – Oct 30 | **Rotation 3 — Physical Design** |
| Week of Nov 2 | Team placement. Members choose, leads confirm |
| Nov 2 – Nov 18 | MAC tile design and hardening |
| Nov 18 | Hard submission gate for the internal competition |
| ~Nov 20 | Internal competition, judged by Dr. Limbrick and an Apple engineer |
| December 2026 | Tiny Tapeout TTSKY26d closes |
| June 2027 | Chips return. Bring-up event |

Blocks run Monday to Friday across two weeks. Each opens with a kickoff session and has
an open lab in the middle. Members work asynchronously in between.

## 6. How the rotation connects to the tapeout

This is not busywork that gets thrown away in November. The rotation exists to make the
December Tiny Tapeout submission survivable for a first-time designer.

- Every rotation project uses the **same Tiny Tapeout pin contract** as the real tile:
  `clk`, `rst_n`, `ena`, `ui_in[7:0]`, `uo_out[7:0]`, `uio_in/uio_out/uio_oe[7:0]`, and a
  `tt_um_` top module name. By November nobody is learning the interface for the first time.
- Verification uses **cocotb + Icarus Verilog**, which is the harness Tiny Tapeout's own
  template ships with. The test file a member writes in Block 2 is structurally the test
  file they submit in November.
- Physical Design uses **LibreLane on sky130**, the same flow that hardens the tile.

By November 2, a member who completed the rotation has already written an FSM, already
written a cocotb test, and already produced a GDS. The MAC tile is then a harder instance
of three things they have each done once.

## 7. Repo layout

```
silicon-aggies-onboarding/
├── README.md                    ← you are here (program plan)
├── setup/
│   └── README.md                ← install everything, once, before Sep 17
├── digital-design/
│   └── README.md                ← Block 1: Traffic Light Controller
├── verification/
│   └── README.md                ← Block 2: Find the Bug
├── physical-design/
│   └── README.md                ← Block 3: Counter to Layout
├── LEADS.md                     ← teaching runbook (leads only)
└── submissions/
    └── <block>/<github-username>/
```

## 8. How you turn work in

Everything goes through this repo. No email attachments, no Discord DMs, no Google Drive
folders.

1. Fork this repo to your own GitHub account (once, at the start of the semester).
2. Make a branch for the block: `git checkout -b block1-yourname`
3. Put your work in `submissions/digital-design/your-github-username/`
4. Push, then open a pull request against `main`.
5. A lead reviews the PR. You either get merged or you get comments and another pass.

This is deliberate. Learning to open a clean pull request is a real deliverable of
onboarding, the PR review *is* the skill check leads use for placement, and the merged
history is a record we can show a sponsor or a judge. It also means every member finishes
the semester with public commits on a chip design project.

## 9. Definition of done, globally

A block is complete when the PR is merged. A PR gets merged when:

- Every file listed in that block's "Deliverables" section is present.
- The thing runs. A lead can clone your branch and reproduce your result from your README.
- The write-up is in your own words and explains what you did, not what the tutorial said.

Late is fine if you tell a lead before the deadline. Silent and missing is not.

## 10. Getting unstuck

Post in `#help` with: what you ran, the full error text, and your OS. Not a screenshot of
a phone photo of a terminal. Leads answer once, in public, so fifty people get the fix.

Before you post, check the "Common problems" table at the bottom of your block's guide.
