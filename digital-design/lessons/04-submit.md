# Lesson 4: Turn in your work

About 20 minutes, and most of that is only the first time.

If you've never used git, that's expected. You need four commands, and you can copy them
from this page every time until you remember them.

---

## Before you start

In your submission folder, run:

```bash
make check
```

Fix anything it lists. Once it says `READY TO SUBMIT`, continue.

## Step 1: Make a branch

A branch is a separate line of work with its own name. Putting your submission on a branch
keeps it apart from the main copy of the repo.

```bash
cd ~/silicon-aggies-onboarding
git checkout -b block1-yourname
```

Use your real name, like `block1-jsmith`.

## Step 2: Choose what to save, then save it

```bash
git status
```

This lists the files git sees as new or changed. You should see your submission folder.
If the list has thousands of files, or any file ending in `.vcd` or `.out`, stop and ask
in the GroupMe. The repo's `.gitignore` file is supposed to hide those.

Then:

```bash
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git commit -m "Block 1: traffic light controller"
```

`git add` tells git which files to include. `git commit` saves a snapshot of them with a
short message describing what you did.

## Step 3: Upload it

```bash
git push -u origin block1-yourname
```

This uploads your branch to **your fork** on GitHub. You only need the `-u origin
block1-yourname` part the first time you push a new branch. After that, `git push` is
enough.

If it asks for a username and password, you skipped the `gh auth login` step in setup. Run
`gh auth login` now (setup Part A4 explains the answers), then push again.

## Step 4: Open the pull request

1. Go to your fork on GitHub (`github.com/YOUR-GITHUB-USERNAME/silicon-aggies-onboarding`).
   You should see a yellow banner offering to open a pull request from the branch you just
   pushed. Click **Compare & pull request**.
2. No banner? Click the **Pull requests** tab, then **New pull request**.
3. Check the two boxes at the top. The left side (base) should be the main ASIC repo,
   `zjohnson2005/silicon-aggies-onboarding`, branch `main`. The right side should be your
   fork and your `block1-yourname` branch.
4. For the title, write `Block 1 - Your Name`.
5. In the description, write a sentence or two for the reviewer: a part you're unsure
   about, or a stretch goal you tried.
6. Click **Create pull request**.

You've turned in Block 1.

---

## What happens next

A lead reviews your pull request within 72 hours. One of two things happens.

**It gets merged.** You're done with Block 1.

**The lead asks for changes.** Something is missing or broken, and there will be specific
comments explaining what. Fix them in the same folder, then run:

```bash
cd ~/silicon-aggies-onboarding
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git commit -m "Address review comments"
git push
```

The pull request updates by itself. Don't open a new one.

Being asked for changes is normal and doesn't count against you. Every company you'd want to
work at reviews code this way.

---

## The four commands, for next time

```bash
git checkout -b branch-name     # start a new branch
git add <folder>                # choose what to include
git commit -m "what you did"    # save a snapshot
git push                        # upload it
```

That covers almost all the git you'll need here. You'll use these again in Blocks 2 and 3,
and by the third time you won't need to look them up.

---

## Late or stuck?

**Tell a lead before the deadline.** Late is fine if you give notice. The people we worry
about are the ones who go quiet. If you hit a wall in week one and disappear, we can't help.

Asking for help never counts against you.
