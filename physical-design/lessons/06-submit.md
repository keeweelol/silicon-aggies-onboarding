# Lesson 6: Turn in your work

About 45 minutes, mostly the write-up.

---

## Step 1: Copy your final layout out of the run folder

The `runs` folder is hundreds of megabytes, and git ignores it on purpose. You only turn in
the one `.gds` file, copied next to your config.

Use the run that matches what's in your `config.yaml` right now. If you kept the Lesson 5
change, that's `second` (or `third`). If you set it back, that's `first`.

```bash
cd ~/silicon-aggies-onboarding/submissions/physical-design/YOUR-GITHUB-USERNAME
cp runs/second/final/gds/counter_sram.gds .
```

(Change `second` to the right run name if needed.)

## Step 2: Check that everything is there

```bash
ls
ls src
```

You should have:

- [ ] `src/counter_sram.sv` (Lesson 2)
- [ ] `config.yaml`, with your Lesson 5 change if that run passed (Lesson 5)
- [ ] `counter_sram.gds` (Step 1 above)
- [ ] `layout.png` and `layout-zoom.png` (Lesson 4)
- [ ] `metrics.md`, with two columns filled in (Lessons 3 and 5)

## Step 3: Write it up

Copy the template:

```bash
cp ../../../physical-design/submission-template/WRITEUP.md .
```

Fill it in, 300 to 500 words. The main part is explaining the six stages from Lesson 0 in
your own words, with numbers from your own run. A lead can tell when it's copied from the
lesson, so describe what *your* design went through.

## Step 4: Branch, commit, and push

Same steps as the last two blocks. [SUBMITTING.md](../../SUBMITTING.md) explains each one.

```bash
cd ~/silicon-aggies-onboarding
git status
git checkout -b block3-YOUR-GITHUB-USERNAME
git add submissions/physical-design/YOUR-GITHUB-USERNAME
git status
```

**Read the second `git status` carefully.** Under **Changes to be committed** it should
show about seven files, all in your folder. If it shows thousands of files, or anything
inside `runs/`, stop and ask in the GroupMe. Don't commit the run folder.

```bash
git commit -m "Block 3: counter-SRAM to layout"
git push -u origin block3-YOUR-GITHUB-USERNAME
```

## Step 5: Open the pull request

1. Go to your fork on GitHub and click **Compare & pull request**.
2. Check it goes from your `block3-...` branch into `main` on
   `zjohnson2005/silicon-aggies-onboarding`.
3. Title it: `Block 3: Your Name (your-github-username)`
4. In the description, write one or two sentences on what you did, plus your DRC error
   count, LVS error count, and WNS.
5. Click **Create pull request**.

If a lead asks for changes, see [how to respond](../../SUBMITTING.md#how-to-respond).

---

That's the whole rotation. You've written a design, found and fixed bugs in one, and turned
one into a chip layout. The MAC tile in November uses all three.

Next up is team placement, the week of Nov 2.
