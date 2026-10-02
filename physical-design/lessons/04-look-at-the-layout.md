# Lesson 4: Look at the layout

**Goal:** open your chip in KLayout, find the parts you learned about in Lesson 0, and take
two screenshots.

> **Windows 10:** KLayout can't open a window from WSL on Windows 10 without extra setup. Do
> this lesson on a Windows 11 or Mac laptop (a friend's is fine). Copy your `.gds` file over,
> or clone your fork there.

---

## Step 1: Open your layout

Inside the LibreLane environment (`nix-shell ~/Su26LLEX/shell.nix` if you're not already
in it), from your submission folder:

```bash
cd ~/silicon-aggies-onboarding/submissions/physical-design/YOUR-GITHUB-USERNAME
klayout runs/first/final/gds/counter_sram.gds
```

Give it a moment to open.

If you only see a few empty boxes with names in them, press `*` (or go to **Display**, then
**Full Hierarchy**). KLayout starts by showing only the top level of the design, and `*`
tells it to draw everything inside.

Press **F2** (or **Display**, then **Zoom Fit**) to fit the whole chip on screen. On most Mac
laptops, F2 changes the screen brightness instead, so hold **fn** and press F2, or use the
menu.

## Step 2: Find your way around

- **Zoom** with the mouse scroll wheel. It zooms toward wherever the mouse is pointing.
- **Pan** by holding the middle mouse button and dragging, or with the arrow keys.
- **Zoom to fit** with F2 (fn+F2 on a Mac) whenever you get lost.

## Step 3: Turn layers on and off

The panel on the right lists the **layers**. Each layer is one kind of material in the chip,
and each gets its own color. In a raw GDS file the layers are numbered instead of named.
These are the ones worth knowing:

| Number | Layer | What it is |
|---|---|---|
| 64/20 | nwell | where the transistors that pull signals up to 1 sit |
| 65/20 | diff | the active silicon where transistors are |
| 66/20 | poly | the transistor gates |
| 67/20 | li1 | the "local interconnect," a thin wiring layer right above the transistors |
| 68/20 | met1 | metal layer 1, the lowest real metal wiring |
| 69/20 | met2 | metal layer 2 |
| 70/20 | met3 | metal layer 3 |
| 71/20 | met4 | metal layer 4 |
| 72/20 | met5 | metal layer 5, the top, used mostly for power |

Try this:

1. Right-click the layer list and choose **Hide All**.
2. Double-click `68/20` to show only met1. Those are real wires.
3. Add `69/20` (met2). Notice that met1 mostly runs one direction and met2 runs the other.
   Routers alternate directions between layers so wires can cross without touching.
4. Add `71/20` and `72/20` (met4 and met5). The thick straight stripes are the power grid
   from the floorplan stage.
5. Right-click and choose **Show All** to bring everything back.

> **Want layer names instead of numbers?** Run
> `librelane --last-run --flow OpenInKLayout config.yaml` from your submission folder. It
> opens the design with the sky130 layer names already set up. It shows a simpler view of
> each cell, so for your screenshots use the GDS view from Step 1.

## Step 4: Find the cells

Zoom in a long way, toward the middle of the chip. Eventually you'll see the design is made
of rows of rectangles, all the same height, lined up side by side. Those are the **standard
cells** from synthesis, sitting where placement put them. Each rectangle is one gate or one
flip-flop.

Many of them are flip-flops. The SRAM's memory alone is 128 of them. You'll also see lots of
small cells that don't do any logic. Those are filler and tap cells, which the flow adds
automatically to keep the rows continuous and connect them to power.

Then zoom all the way back out with F2. That whole picture is your counter and its 16-slot
memory.

## Step 5: Take two screenshots

**Screenshot 1: the whole chip.** Press F2 so the whole chip fits, with all layers on. Save
it as `layout.png` in your submission folder.

**Screenshot 2: zoomed in.** Zoom in until you can clearly see individual cells in their
rows, and some wires connecting them. Save it as `layout-zoom.png` in your submission folder.

The zoomed-in one is the picture that makes sense to someone who's never seen a chip layout
before. It's worth making it a good one.

> **How to screenshot:** on Windows, press Windows+Shift+S and drag a box, then paste into
> Paint and save. On a Mac, press Cmd+Shift+4 and drag a box. It lands on your Desktop.
> Move each one into your submission folder right after you take it, with
> `mv ~/Desktop/Screenshot*.png layout.png` (then `layout-zoom.png` for the second one). On
> Linux, KLayout can also save the view directly: **File**, then **Screenshot**.

---

## Before you move on

- [ ] You opened your layout and found the metal layers and the rows of cells.
- [ ] `layout.png` and `layout-zoom.png` are saved in your submission folder.

---

**Next:** [Lesson 5: Change one thing](05-change-one-thing.md).
