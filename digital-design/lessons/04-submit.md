# Lesson 4 — Submit your work

Twenty minutes, and most of it is the first time only.

If you have never used git, that's expected. You need four commands and you can copy them
from here every time until they stick.

---

## First, check yourself

```bash
make check
```

Fix anything it lists. When it says `READY TO SUBMIT`, keep going.

## Step 1 — Make a branch

A branch is a named copy of your work so you don't disturb `main`.

```bash
cd ~/silicon-aggies-onboarding
git checkout -b block1-yourname
```

Use your actual name: `block1-jsmith`.

## Step 2 — Stage and commit

```bash
git add submissions/digital-design/YOUR-GITHUB-USERNAME
git commit -m "Block 1: traffic light controller"
```

`git add` says "include these files." `git commit` saves a snapshot with a message
attached.

Run `git status` first if you want to see what's about to be included. If it lists
thousands of files or anything with `.vcd` or `.out`, stop and ask — the `.gitignore`
should be catching those.

## Step 3 — Push

```bash
git push -u origin block1-yourname
```

This uploads your branch to **your fork** on GitHub. The `-u origin block1-yourname` part
is only needed the first time you push a given branch.

If it asks for a password, that's the thing GitHub stopped supporting — you need a
personal access token instead. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md).

## Step 4 — Open the pull request

1. Go to your fork on GitHub. There should be a banner offering to open a pull request
   from the branch you just pushed. Click it.
2. If there's no banner: **Pull requests** tab → **New pull request**.
3. Make sure it's going **from** your branch **into** the org repo's `main`.
4. Title it: `Block 1 — Your Name`
5. In the description, write one or two sentences. Anything you want a reviewer to know —
   a part you're unsure about, a stretch goal you tried.
6. **Create pull request.**

Done. You've submitted.

---

## What happens next

A lead reviews within 72 hours. One of two things:

**Merged.** You're done with Block 1.

**Changes requested.** Something is missing or broken. There'll be specific comments. Fix
them in your same folder, then:

```bash
git add .
git commit -m "Address review comments"
git push
```

The pull request updates automatically — you don't open a new one.

Changes requested is completely normal and is not a mark against you. It's how code review
works everywhere, including at every company any of us want to work at.

---

## The four commands, for next time

```bash
git checkout -b branch-name     # start working on something
git add .                       # include your changes
git commit -m "what you did"    # save a snapshot
git push                        # upload it
```

That's 95% of git for what we do. You'll run these two more times this semester, in Blocks
2 and 3, and by the third one you won't need to look them up.

---

## Late or stuck?

**Tell a lead before the deadline.** Late with notice is fine. What we chase is people who
go quiet — if you hit a wall in week one and disappear, we can't help.

There is no version of this where asking for help counts against you.
