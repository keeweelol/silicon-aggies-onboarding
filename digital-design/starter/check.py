#!/usr/bin/env python3
"""
ASIC Block 1 submission checker.

Run this before you open your pull request:

    make check

It checks the same things a lead checks, so you can fix problems before
anyone else sees them. It does not grade you and it does not send anything
anywhere. It just runs on your machine and prints a list.
"""

import glob
import os
import re
import subprocess
import sys

OK = "  [ok]     "
NO = "  [MISSING]"
BAD = "  [PROBLEM]"

problems = []


def ok(msg):
    print(OK + msg)


def missing(msg, why):
    print(NO + " " + msg)
    problems.append(why)


def bad(msg, why):
    print(BAD + " " + msg)
    problems.append(why)


def find(patterns):
    """Return the first file matching any of these glob patterns."""
    for p in patterns:
        hits = glob.glob(p)
        if hits:
            return hits[0]
    return None


print()
print("=" * 55)
print("  Block 1 submission check")
print("=" * 55)
print()

# ================================================================ files
print("FILES")

design = find(["tt_um_traffic_light.v"])
if design:
    ok("tt_um_traffic_light.v")
else:
    missing("tt_um_traffic_light.v", "Your design file is not in this folder.")

diagram = find(["state-diagram.*", "state_diagram.*"])
if diagram:
    ok(f"state diagram ({diagram})")
else:
    missing(
        "state-diagram.jpg / .png",
        "No state diagram. Photograph the one you drew and save it here.",
    )

wave = find(["waveform.*"])
if wave:
    ok(f"waveform screenshot ({wave})")
else:
    missing(
        "waveform.png",
        "No waveform screenshot. Run `make wave`, then screenshot GTKWave.",
    )

writeup = find(["WRITEUP.md"])
if writeup:
    words = len(open(writeup, encoding="utf-8", errors="ignore").read().split())
    if words < 250:
        bad(
            f"WRITEUP.md is only {words} words",
            f"Your write-up is {words} words. The target is 300-500.",
        )
    else:
        ok(f"WRITEUP.md ({words} words)")

    text = open(writeup, encoding="utf-8", errors="ignore").read()
    if "TODO" in text or "<your answer" in text.lower():
        bad(
            "WRITEUP.md still has template placeholders in it",
            "Your write-up still contains TODO or placeholder text.",
        )
else:
    missing("WRITEUP.md", "No write-up. Copy the template and fill it in.")

print()

# ================================================================ build
print("BUILD AND TEST")

if not design:
    bad("cannot run tests without a design file", "Design file missing, skipped tests.")
else:
    build = subprocess.run(
        ["iverilog", "-g2012", "-o", "check.out", "tb_traffic_light.v", design],
        capture_output=True,
        text=True,
    )
    if build.returncode != 0:
        bad("design does not compile", "Your design does not compile. Run `make` to see the errors.")
        print()
        print(build.stderr.strip()[:800])
    else:
        ok("compiles with no errors")

        run = subprocess.run(["./check.out"], capture_output=True, text=True, timeout=120)
        out = run.stdout

        n_pass = out.count("[PASS]")
        n_fail = out.count("[FAIL]")

        if "TIMEOUT" in out:
            bad(
                "simulation timed out",
                "The simulation hung. Your design never reaches a state the test waits for.",
            )
        elif n_fail == 0 and n_pass >= 10:
            ok(f"all {n_pass} behavior checks pass")
        else:
            bad(
                f"{n_pass} checks pass, {n_fail} fail",
                f"{n_fail} behavior check(s) still failing. Run `make` for details.",
            )
            for line in out.splitlines():
                if "[FAIL]" in line:
                    print("           " + line.strip())

        os.remove("check.out")

print()

# ================================================================ verdict
print("=" * 55)
if not problems:
    print("  READY TO SUBMIT")
    print()
    print("  git checkout -b block1-yourname")
    print("  git add .")
    print('  git commit -m "Block 1: traffic light controller"')
    print("  git push -u origin block1-yourname")
    print()
    print("  Then open the pull request on GitHub.")
else:
    print(f"  NOT READY: {len(problems)} thing(s) to fix")
    print()
    for i, p in enumerate(problems, 1):
        print(f"  {i}. {p}")
    print()
    print("  Stuck on one of these? Check digital-design/TROUBLESHOOTING.md, then ask in the GroupMe.")
print("=" * 55)
print()

sys.exit(1 if problems else 0)
