# How to turn in your work

Every block is turned in the same way: **one folder, one branch, one pull request.** This
page covers all three blocks. Each block's last lesson walks you through the parts that are
specific to that block, then sends you here for the pull request.

If you've never opened a pull request, that's expected. Follow the steps in order and copy
the commands.

---

## 1. Put your files in the right place

Everything you turn in goes in one folder named after your GitHub username:

```
submissions/<block>/<your-github-username>/
```

Use these exact file names. Leads look for them by name, so `Waveform.PNG` or
`writeup.md` makes your submission harder to review.

**Block 1:** `submissions/digital-design/YOUR-GITHUB-USERNAME/`

```
tt_um_traffic_light.v     your design
state-diagram.jpg         photo of your hand-drawn state diagram (.png is fine too)
waveform.png              GTKWave screenshot
WRITEUP.md                your write-up
```

The starter files you copied in Lesson 1 (`Makefile`, `check.py`, and the testbenches) can
stay in the folder. Leads ignore them.

**Block 2:** `submissions/verification/YOUR-GITHUB-USERNAME/`

```
buggy_counter/
    buggy_design/counter.sv          fixed counter
    testbench/counter_tb.sv          your testbench
buggy_counter_sram/
    buggy_design/counter_sram.sv     fixed counter-SRAM
    testbench/buggy_cosram_tb.sv     your finished testbench
waveform-counter.png
waveform-counter-sram.png
WRITEUP.md
```

**Block 3:** `submissions/physical-design/YOUR-GITHUB-USERNAME/`

```
src/counter_sram.sv
config.yaml
counter_sram.gds
layout.png
layout-zoom.png
metrics.md
WRITEUP.md
```

Don't include build output: no `obj_dir/`, no `.vcd` files, and no `runs/` folder. The
repo's `.gitignore` hides these for you, but check anyway in step 3.

## 2. Start from `main`, then make a branch

A **branch** is a separate line of work with its own name. Each block gets its own branch,
so one block's review never gets mixed up with another's.

```bash
cd ~/silicon-aggies-onboarding
git status
```

The first line of `git status` says which branch you're on. You should be on `main`,
because each block's first lesson has you switch to it. If you're on an older block's
branch instead, ask in the GroupMe before going on.

Now make the branch for this block. Use the block number and your GitHub username:

```bash
git checkout -b block1-YOUR-GITHUB-USERNAME
```

(For Block 2 it's `block2-...`, for Block 3 it's `block3-...`. If you already made a Block 1
branch with a different name, keep using it. The name doesn't have to be perfect.)

## 3. Add only your folder, and check what's included

```bash
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git status
```

(Use `verification` or `physical-design` instead of `digital-design` for Blocks 2 and 3.)

Read the list under **Changes to be committed**. It should show only files inside your
folder, and roughly the number of files listed in step 1. If you see files from anywhere
else, or hundreds of files, stop and ask in the GroupMe.

## 4. Commit and push

```bash
git commit -m "Block 1: traffic light controller"
git push -u origin block1-YOUR-GITHUB-USERNAME
```

`git commit` saves a snapshot with a short message. `git push` uploads your branch to your
fork on GitHub.

If `git push` asks for a password, run `gh auth login` (setup Part A4) and push again.

## 5. Open the pull request

1. Go to your fork: `github.com/YOUR-GITHUB-USERNAME/silicon-aggies-onboarding`. You should
   see a yellow banner. Click **Compare & pull request**.
   No banner? Click the **Pull requests** tab, then **New pull request**, then
   **compare across forks**, and pick your branch on the right.
2. Check the bar at the top. It should read, left to right:
   **base repository:** `zjohnson2005/silicon-aggies-onboarding`, **base:** `main`, then
   **head repository:** your fork, **compare:** your `blockN-...` branch.
3. **Title** it in exactly this format, so leads can sort them:

   ```
   Block 1: Jane Smith (jsmith)
   ```

   That's the block number, your full name, and your GitHub username in parentheses.
4. **Write a short description:** one or two sentences on what you did, plus anything you'd
   like a lead to look at closely. If something is missing or late, say so here.
5. Click **Create pull request**.

You've turned in the block.

---

## 6. What happens next

A lead reviews your pull request within **72 hours**. You'll get an email from GitHub when
they do, and it also shows up on the pull request page.

The lead does one of two things:

- **Approves and merges it.** The pull request turns purple and says **Merged**. You're done
  with that block.
- **Requests changes.** The lead leaves comments, usually on specific lines of your files.
  This is normal. Most submissions get at least one round of comments.

### How to read the comments

Leads start every comment with one of these labels:

| Label | What it means | What you do |
|---|---|---|
| **Must fix:** | Something is missing, broken, or doesn't meet the block's requirements | Fix it before the pull request can be merged |
| **Suggestion:** | An idea to make it better | Up to you. Try it if you have time, or reply saying why you didn't |
| **Question:** | The lead wants to understand your thinking | Reply to the comment with an answer |
| **Nice:** | Something you did well | Nothing. Enjoy it |

Only **Must fix** comments block your merge.

### How to respond

1. Make the fixes in the same folder, on the same branch. Don't make a new branch, and don't
   open a new pull request.
2. Save and upload:

   ```bash
   cd ~/silicon-aggies-onboarding
   git add submissions/digital-design/YOUR-GITHUB-USERNAME
   git commit -m "Address review comments"
   git push
   ```

   The pull request updates by itself.
3. On GitHub, reply to each **Must fix** comment with a short note, like "Fixed: moved the
   timer reset into every transition." Then click **Resolve conversation**.
4. Near the top right of the pull request, next to the lead's name under **Reviewers**,
   click the circular arrow icon to **re-request review**. That tells the lead you're ready
   for another look.

If you disagree with a comment, say so in a reply and explain why. That's a normal part of
code review, and sometimes the lead will agree with you.

---

## Before you submit, check these

- [ ] Every file from step 1 is there, spelled exactly the same.
- [ ] Your write-up has no leftover template text (no `<your answer here>`, no instructions
      in italics).
- [ ] Your screenshots are readable: signal names visible, not a tiny thumbnail.
- [ ] For Block 1, `make check` says `READY TO SUBMIT`.
- [ ] For Block 2, both simulations end with `Verilog $finish` and no `%Error`.
- [ ] For Block 3, 0 DRC errors, 0 LVS errors, and WNS zero or positive.

## Late or stuck?

Tell a lead **before** the deadline. Late with notice is fine. If you open the pull request
late, say so in the description.

For git problems, see the git section of
[Block 1's troubleshooting page](digital-design/TROUBLESHOOTING.md#git-and-github).
