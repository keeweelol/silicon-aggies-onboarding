# Lesson 4: Turn in your work

About 20 minutes, and most of that is only the first time.

If you've never used git, that's expected. Every block is turned in the same way, and the
full steps are in [SUBMITTING.md](../../SUBMITTING.md) at the top of the repo. This lesson
walks you through it for Block 1.

---

## Step 1: Check your work

In your submission folder, run:

```bash
cd ~/silicon-aggies-onboarding/submissions/digital-design/YOUR-GITHUB-USERNAME
make check
```

Fix anything it lists. Once it says `READY TO SUBMIT`, check the file names one more time:

```bash
ls
```

You need these four, spelled exactly like this:

| File | What it is |
|---|---|
| `tt_um_traffic_light.v` | your design |
| `state-diagram.jpg` | photo of your state diagram (`.png` is fine) |
| `waveform.png` | GTKWave screenshot |
| `WRITEUP.md` | your write-up |

The other starter files (`Makefile`, `check.py`, and the testbenches) can stay.

## Step 2: Make a branch

A **branch** is a separate line of work with its own name. Each block gets its own branch.

```bash
cd ~/silicon-aggies-onboarding
git status
```

The first line should say `On branch main`. Then:

```bash
git checkout -b block1-YOUR-GITHUB-USERNAME
```

## Step 3: Add your folder, and check what's included

```bash
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git status
```

Read the list under **Changes to be committed**. It should only show files in your folder.
If you see hundreds of files, or files ending in `.vcd` or `.out`, stop and ask in the
GroupMe.

## Step 4: Commit and push

```bash
git commit -m "Block 1: traffic light controller"
git push -u origin block1-YOUR-GITHUB-USERNAME
```

`git commit` saves a snapshot of your files with a short message. `git push` uploads your
branch to your fork on GitHub.

If `git push` asks for a password, you skipped `gh auth login` in setup. Run it now (setup
Part A4 explains the answers), then push again.

## Step 5: Open the pull request

1. Go to your fork on GitHub (`github.com/YOUR-GITHUB-USERNAME/silicon-aggies-onboarding`)
   and click **Compare & pull request** on the yellow banner.
2. Check the bar at the top. The left side should be
   `zjohnson2005/silicon-aggies-onboarding` and `main`. The right side should be your fork
   and your `block1-...` branch.
3. Title it exactly like this, with your name and username:

   ```
   Block 1: Jane Smith (jsmith)
   ```

4. In the description, write one or two sentences on what you built, plus anything you'd
   like a lead to look at closely.
5. Click **Create pull request**.

You've turned in Block 1.

---

## What happens next

A lead reviews your pull request within 72 hours, and GitHub emails you when they do. Either
it gets **merged** (you're done), or the lead **requests changes** and leaves comments.

Getting comments is normal. Leads label every comment so you know what matters:

- **Must fix:** has to be fixed before the pull request is merged.
- **Suggestion:** an idea. Up to you.
- **Question:** reply with an answer.
- **Nice:** something you did well.

To respond, fix things in the same folder, then:

```bash
cd ~/silicon-aggies-onboarding
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git commit -m "Address review comments"
git push
```

The pull request updates by itself. Don't open a new one. Reply to each **Must fix**
comment saying what you changed, then click **re-request review** (the circular arrow next
to the lead's name, under **Reviewers**). [SUBMITTING.md](../../SUBMITTING.md#6-what-happens-next)
has more detail.

---

## The four commands, for next time

```bash
git checkout -b branch-name     # start a new branch
git add <folder>                # choose what to include
git commit -m "what you did"    # save a snapshot
git push                        # upload it
```

You'll use these again in Blocks 2 and 3, and by the third time you won't need to look
them up.

---

## Late or stuck?

**Tell a lead before the deadline.** Late is fine if you give notice. The people we worry
about are the ones who go quiet. If you hit a wall in week one and disappear, we can't help.

Asking for help never counts against you.
