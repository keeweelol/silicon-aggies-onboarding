#!/usr/bin/env python3
"""
Automatic check for ASIC onboarding pull requests.

GitHub runs this on every pull request that touches submissions/. You can also
run it yourself before you push, from the top of the repo:

    python3 .github/scripts/check_submission.py submissions/verification/YOUR-GITHUB-USERNAME

It checks the same things a lead checks first: the files are all there, the
designs build and behave like the golden versions, the testbenches catch the
planted bugs, and the write-up has no template text left in it. A lead still
reviews every pull request. Passing this check means it's ready for that review.
"""

import argparse
import concurrent.futures
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXTRA_TB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tb")
BLOCKS = ("digital-design", "verification", "physical-design")


# ====================================================================== results
class Report:
    def __init__(self):
        self.lines = []      # (status, title, detail)
        self.problems = 0

    def ok(self, title):
        self.lines.append(("ok", title, ""))

    def bad(self, title, detail=""):
        self.lines.append(("bad", title, detail))
        self.problems += 1

    def note(self, title, detail=""):
        self.lines.append(("note", title, detail))

    def section(self, title):
        self.lines.append(("section", title, ""))

    def print_terminal(self):
        tags = {"ok": "  [ok]      ", "bad": "  [PROBLEM] ", "note": "  [note]    "}
        for status, title, detail in self.lines:
            if status == "section":
                print()
                print(title.upper())
                continue
            print(tags[status] + title)
            for d in detail.splitlines():
                print("              " + d)
        print()
        print("=" * 60)
        if self.problems:
            print(f"  NOT READY: {self.problems} problem(s). Fix them, then push again.")
        else:
            print("  PASSED. A lead will review your pull request next.")
        print("=" * 60)

    def markdown(self, heading):
        icon = {"ok": "✅", "bad": "❌", "note": "ℹ️"}
        out = [f"## {heading}", ""]
        if self.problems:
            out.append(f"**{self.problems} problem(s) to fix.** Fix them in your folder, "
                       "commit, and push. This check runs again by itself.")
        else:
            out.append("**Everything passed.** A lead will review your pull request next.")
        for status, title, detail in self.lines:
            if status == "section":
                out += ["", f"### {title}", ""]
                continue
            out.append(f"- {icon[status]} {title}")
            if detail:
                out.append("")
                out.append("  ```")
                out += ["  " + d for d in detail.splitlines()]
                out.append("  ```")
        out += ["", "Stuck? Check the block's TROUBLESHOOTING.md, then ask in the ASIC GroupMe."]
        return "\n".join(out) + "\n"


# ====================================================================== helpers
def read_text(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def require_files(rep, folder, names):
    """Check every file exists. Point out near-misses like Waveform.PNG."""
    present = set()
    for root, _dirs, files in os.walk(folder):
        for f in files:
            present.add(os.path.relpath(os.path.join(root, f), folder))
    lower = {p.lower(): p for p in present}
    all_ok = True
    for name in names:
        if name in present:
            continue
        all_ok = False
        if name.lower() in lower:
            rep.bad(f"`{lower[name.lower()]}` has to be named exactly `{name}`",
                    "Leads look for files by their exact names, capitals included.")
        else:
            rep.bad(f"missing `{name}`")
    if all_ok:
        rep.ok(f"all {len(names)} required files are there")
    return all_ok


def check_image(rep, path, label):
    """Make sure a screenshot or photo is a real PNG or JPEG that GitHub can show."""
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        head = f.read(12)
    size = os.path.getsize(path)
    if head.startswith(b"\x89PNG") or head.startswith(b"\xff\xd8\xff"):
        if size < 2000:
            rep.bad(f"`{label}` is only {size} bytes", "That's too small to be a readable screenshot.")
        else:
            rep.ok(f"`{label}` is a real image")
    elif b"ftyp" in head:
        rep.bad(f"`{label}` is a HEIC photo, not a PNG or JPEG",
                "GitHub can't show HEIC. Re-save it as .jpg or .png "
                "(on an iPhone: screenshot the photo, or Settings > Camera > Formats > Most Compatible).")
    else:
        rep.bad(f"`{label}` isn't a PNG or JPEG image", "Re-save the screenshot as a .png.")


def check_writeup(rep, path, template_path, min_words=250):
    """Word count, plus anything left over from the template."""
    if not os.path.exists(path):
        return
    text = read_text(path)
    flat = " ".join(text.split())
    words = len(text.split())
    if words < min_words:
        rep.bad(f"`WRITEUP.md` is only {words} words", "The target is 300 to 500 words.")
    else:
        rep.ok(f"`WRITEUP.md` is {words} words")

    leftovers = []
    for marker in ("<your answer", "YOUR NAME", "<file name>", "<line number>"):
        if marker.lower() in text.lower():
            leftovers.append(marker)
    if os.path.exists(template_path):
        template = read_text(template_path)
        for m in re.finditer(r"(?<![*\w])\*(?!\*)(.+?)(?<!\*)\*(?![*\w])", template, re.DOTALL):
            words_in = " ".join(m.group(1).split()).split()
            if len(words_in) < 6:
                continue
            probe = " ".join(words_in[:8])
            if probe in flat:
                leftovers.append(f'instructions: "{" ".join(words_in[:6])}..."')
    if leftovers:
        rep.bad("`WRITEUP.md` still has template text in it",
                "Replace or delete these (delete an optional section you skipped, heading too):\n"
                + "\n".join("  " + x for x in leftovers[:8]))
    else:
        rep.ok("`WRITEUP.md` has no template text left in it")
    return text


# ====================================================================== VCD
def parse_vcd(path):
    """Return {full_signal_name: id} and the list of (time, id, value) changes."""
    names, changes, scope, t = {}, [], [], 0
    with open(path, encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("$scope"):
                scope.append(line.split()[2])
            elif line.startswith("$upscope"):
                scope.pop()
            elif line.startswith("$var"):
                p = line.split()
                names[".".join(scope + [p[4]])] = p[3]
            elif line.startswith("$"):
                continue
            elif line[0] == "#":
                t = int(line[1:])
            elif line[0] in "bB":
                v, i = line[1:].split()
                changes.append((t, i, v))
            elif line[0] in "01xzXZ":
                changes.append((t, line[1:], line[0]))
    return names, changes


def dut_trace(vcd_path, ports):
    """Values of the DUT's ports just before every rising clock edge.

    Finds the DUT as the scope directly inside `test` that has every one of
    `ports`, so it works whatever the student named the instance.
    """
    names, changes = parse_vcd(vcd_path)
    scope = None
    for full in names:
        parts = full.split(".")
        if len(parts) >= 3 and parts[-3] == "test":
            cand = ".".join(parts[:-1])
            if all(f"{cand}.{p}" in names for p in ports):
                scope = cand
                break
    if scope is None:
        return None
    ids = {p: names[f"{scope}.{p}"] for p in ports}
    clk = ids["clk"]
    cur, rows, prev = {}, [], "0"
    i = 0
    while i < len(changes):
        t = changes[i][0]
        group = []
        while i < len(changes) and changes[i][0] == t:
            group.append(changes[i])
            i += 1
        new = next((v for _, cid, v in group if cid == clk), prev)
        if prev == "0" and new == "1":
            rows.append({p: cur.get(ids[p], "x") for p in ports if p != "clk"})
        for _, cid, v in group:
            cur[cid] = v
        prev = new
    return rows


def as_int(v):
    v = v.lstrip("b")
    return int(v, 2) if v and set(v) <= set("01") else None


# ====================================================================== simulation
class Sim:
    """Builds and runs Verilator simulations in a scratch folder."""

    def __init__(self):
        self.tmp = tempfile.mkdtemp(prefix="asic-check-")
        self.cache = {}

    def prefetch(self, jobs):
        """Run many (design, tb, ports) simulations at once, one per CPU core."""
        todo = [j for j in jobs if os.path.exists(j[0]) and os.path.exists(j[1])]
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as pool:
            list(pool.map(lambda j: self.run(*j), todo))

    def run(self, design, tb, ports):
        """Return (trace, error_text). trace is None if it failed."""
        key = (os.path.abspath(design), os.path.abspath(tb), tuple(ports))
        if key not in self.cache:
            self.cache[key] = self._run(design, tb, ports)
        return self.cache[key]

    def _run(self, design, tb, ports):
        work = tempfile.mkdtemp(dir=self.tmp)
        # Same flags the lessons use, plus -O0, which only makes the C++ build faster.
        build = subprocess.run(
            ["verilator", "--binary", "--timing", "--trace", "--top-module", "test",
             "-CFLAGS", "-O0", "-Mdir", "obj_dir", os.path.abspath(design), os.path.abspath(tb)],
            cwd=work, capture_output=True, text=True,
        )
        if build.returncode != 0:
            errs = [l.replace(REPO + os.sep, "") for l in (build.stdout + build.stderr).splitlines()
                    if l.startswith("%")]
            return None, "\n".join(errs[:6]) or "the build failed"
        try:
            run = subprocess.run(["./obj_dir/Vtest"], cwd=work, capture_output=True,
                                 text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return None, "the simulation never finished (is $finish missing?)"
        if "$finish" not in run.stdout + run.stderr:
            return None, "the simulation didn't reach $finish"
        vcd = os.path.join(work, "dump.vcd")
        if not os.path.exists(vcd):
            return None, 'no dump.vcd (is $dumpfile("dump.vcd") missing?)'
        trace = dut_trace(vcd, ports)
        if trace is None:
            return None, ("couldn't find the design's signals in the waveform. "
                          "Is the testbench module named `test`, with the design created inside it?")
        return trace, ""

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


def make_variant(src, fixes, dest):
    """Copy `src`, applying each (old, new) replacement. Used to build designs
    with exactly one planted bug left in."""
    text = read_text(src)
    for old, new in fixes:
        if old not in text:
            raise RuntimeError(f"internal: expected `{old}` in {src}. Has the exercise changed?")
        text = text.replace(old, new, 1)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    return dest


def first_difference(a, b):
    for i, (ra, rb) in enumerate(zip(a, b)):
        if ra != rb:
            return i, ra, rb
    if len(a) != len(b):
        return min(len(a), len(b)), None, None
    return None


def fmt_row(row):
    if row is None:
        return "(simulation ended)"
    return ", ".join(f"{k}={as_int(v) if as_int(v) is not None else v}" for k, v in row.items())


def check_design_matches_golden(rep, sim, design, golden, tbs, ports, label):
    """Run each testbench on the student's design and the golden one. They must match."""
    for tb_label, tb in tbs:
        mine, err = sim.run(design, tb, ports)
        if mine is None:
            rep.bad(f"{label} doesn't build or run with {tb_label}", err)
            return False
        gold, err = sim.run(golden, tb, ports)
        if gold is None:
            rep.bad(f"internal: the golden design failed with {tb_label}", err)
            return False
        diff = first_difference(mine, gold)
        if diff:
            i, r_mine, r_gold = diff
            rep.bad(f"{label} doesn't behave like the golden design ({tb_label})",
                    f"First difference, at clock edge {i}:\n"
                    f"  yours:  {fmt_row(r_mine)}\n"
                    f"  golden: {fmt_row(r_gold)}\n"
                    "A bug is still in there, or a fix changed something else.")
            return False
    if any(name == "your testbench" for name, _ in tbs):
        rep.ok(f"{label} matches the golden design, on your inputs and on extra random ones")
    else:
        rep.ok(f"{label} matches the golden design, on the golden testbench and extra random inputs")
    return True


def check_tb_catches_bugs(rep, sim, tb, golden, variants, ports, label):
    """The student's testbench has to make every planted bug visible."""
    gold, err = sim.run(golden, tb, ports)
    if gold is None:
        rep.bad(f"{label} doesn't build or run", err)
        return None
    missed = []
    for bug_label, design in variants:
        trace, err = sim.run(design, tb, ports)
        if trace is not None and not first_difference(trace, gold):
            missed.append(bug_label)
    if missed:
        rep.bad(f"{label} misses {len(missed)} of the {len(variants)} planted bugs",
                "With only this bug in the design, your waveform looks exactly like the "
                "golden one:\n" + "\n".join("  " + m for m in missed)
                + "\nAdd test steps that make it show up (the spec lines in the lesson).")
    else:
        how_many = "both" if len(variants) == 2 else f"all {len(variants)}"
        rep.ok(f"{label} catches {how_many} planted bugs, each one on its own")
    return gold


# ====================================================================== Block 1
def check_block1(rep, folder):
    rep.section("Images")
    found = False
    for f in sorted(os.listdir(folder)):
        if f.lower().startswith(("state-diagram", "state_diagram", "waveform.")):
            check_image(rep, os.path.join(folder, f), f)
            found = True
    if not found:
        rep.note("no images yet (the next section says which are missing)")

    rep.section("Design and write-up (the same checks as `make check`)")
    with tempfile.TemporaryDirectory() as tmp:
        for f in os.listdir(folder):
            p = os.path.join(folder, f)
            if os.path.isfile(p):
                shutil.copy(p, tmp)
        # Always use the repo's own testbench and checker, not the copies in the folder.
        starter = os.path.join(REPO, "digital-design", "starter")
        for f in ("tb_traffic_light.v", "check.py"):
            shutil.copy(os.path.join(starter, f), tmp)
        run = subprocess.run([sys.executable, "check.py"], cwd=tmp, capture_output=True,
                             text=True, timeout=300)
        out = run.stdout
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("[ok]"):
            rep.ok(s[4:].strip())
        elif s.startswith("[PROBLEM]") or s.startswith("[MISSING]"):
            rep.bad(s.split("]", 1)[1].strip())
        elif s.startswith("[FAIL]"):
            rep.lines[-1] = (rep.lines[-1][0], rep.lines[-1][1],
                             (rep.lines[-1][2] + "\n" + s).strip())


# ====================================================================== Block 2
COUNTER_PORTS = ["clk", "rst_n", "en", "count"]
SRAM_PORTS = ["clk", "rst_n", "en", "write_en", "write_data", "address", "read_data"]


def counter_coverage(trace):
    """Which counter spec lines the testbench actually made happen."""
    missing = []
    vals = [{k: as_int(v) for k, v in r.items()} for r in trace]
    if not any(r["rst_n"] == 0 for r in vals):
        missing.append("spec 1: reset (rst_n = 0) never happens")
    if not any(a["rst_n"] == 1 and a["en"] == 1 and a["count"] == 15 and b["count"] == 0
               for a, b in zip(vals, vals[1:])):
        missing.append("spec 4: the count never goes from 15 back to 0")
    if not any(r["rst_n"] == 1 and r["en"] == 0 for r in vals[1:]):
        missing.append("spec 3: en is never 0 while the counter is running")
    if not any(r["rst_n"] == 0 and r["count"] not in (0, None) for r in vals):
        missing.append("spec 1: no reset in the middle of counting")
    return missing


def sram_coverage(trace):
    missing = []
    vals = [{k: as_int(v) for k, v in r.items()} for r in trace]
    written = {r["address"] for r in vals if r["rst_n"] == 1 and r["write_en"] == 1}
    read = {r["address"] for r in vals if r["rst_n"] == 1 and r["write_en"] == 0}
    if len(written - {None}) < 16:
        missing.append(f"spec 2: only {len(written - {None})} of the 16 slots get written")
    if len(read - {None}) < 16:
        missing.append(f"spec 3/4: only {len(read - {None})} of the 16 slots get read back with write_en = 0")
    return missing


def check_block2(rep, folder, sim):
    rep.section("Files")
    names = [
        "buggy_counter/buggy_design/counter.sv",
        "buggy_counter/testbench/counter_tb.sv",
        "buggy_counter_sram/buggy_design/counter_sram.sv",
        "buggy_counter_sram/testbench/buggy_cosram_tb.sv",
        "waveform-counter.png",
        "waveform-counter-sram.png",
        "WRITEUP.md",
    ]
    require_files(rep, folder, names)
    for img in ("waveform-counter.png", "waveform-counter-sram.png"):
        check_image(rep, os.path.join(folder, img), img)

    v = os.path.join(REPO, "verification")
    tmp = sim.tmp

    # ---- counter
    rep.section("Counter (Lesson 2)")
    my_design = os.path.join(folder, "buggy_counter/buggy_design/counter.sv")
    my_tb = os.path.join(folder, "buggy_counter/testbench/counter_tb.sv")
    golden = os.path.join(v, "golden_counter/counter_design/counter.sv")
    buggy = os.path.join(v, "buggy_counter/buggy_design/counter.sv")
    fix_polarity = ("if (rst_n) begin", "if (!rst_n) begin")
    fix_value = ("count <= 4'd5;", "count <= 4'd0;")
    variants = [
        ("the reset checks the wrong value of rst_n",
         make_variant(buggy, [fix_value], os.path.join(tmp, "cnt_bug_polarity.sv"))),
        ("reset sets count to the wrong value",
         make_variant(buggy, [fix_polarity], os.path.join(tmp, "cnt_bug_value.sv"))),
    ]
    tbs = [("the golden testbench", os.path.join(v, "golden_counter/testbench/counter_tb.sv")),
           ("extra random inputs", os.path.join(EXTRA_TB, "counter_extra_tb.sv"))]
    if os.path.exists(my_tb):
        tbs.insert(0, ("your testbench", my_tb))
    sim.prefetch([(d, my_tb, COUNTER_PORTS) for _, d in variants]
                 + [(d, tb, COUNTER_PORTS) for d in (my_design, golden) for _, tb in tbs])
    if os.path.exists(my_tb):
        gold = check_tb_catches_bugs(rep, sim, my_tb, golden, variants, COUNTER_PORTS, "your counter testbench")
        if gold is None:
            tbs = tbs[1:]          # already reported; check the design with the other testbenches
        else:
            gaps = counter_coverage(gold)
            if gaps:
                rep.bad("your counter testbench doesn't make every spec line happen",
                        "\n".join(gaps))
            else:
                rep.ok("your counter testbench makes all four spec lines happen")
    if os.path.exists(my_design):
        check_design_matches_golden(rep, sim, my_design, golden, tbs, COUNTER_PORTS, "your fixed counter")

    # ---- counter-SRAM
    rep.section("Counter-SRAM (Lesson 4)")
    my_design = os.path.join(folder, "buggy_counter_sram/buggy_design/counter_sram.sv")
    my_tb = os.path.join(folder, "buggy_counter_sram/testbench/buggy_cosram_tb.sv")
    golden = os.path.join(v, "golden_counter_sram/counter_sram_design/counter_sram.sv")
    buggy = os.path.join(v, "buggy_counter_sram/buggy_design/counter_sram.sv")
    fix_en = ("else if (!en) begin", "else if (en) begin")
    fix_edge = ("always_ff @(negedge clk) begin", "always_ff @(posedge clk) begin")
    fix_we = ("if (!write_en) begin", "if (write_en) begin")
    variants = [
        ("the counter counts when en is 0",
         make_variant(buggy, [fix_edge, fix_we], os.path.join(tmp, "sram_bug_en.sv"))),
        ("the SRAM runs on the wrong clock edge",
         make_variant(buggy, [fix_en, fix_we], os.path.join(tmp, "sram_bug_edge.sv"))),
        ("the SRAM writes when write_en is 0",
         make_variant(buggy, [fix_en, fix_edge], os.path.join(tmp, "sram_bug_we.sv"))),
    ]
    tbs = [("the golden testbench", os.path.join(v, "golden_counter_sram/testbench/counter_sram_tb.sv")),
           ("extra random inputs", os.path.join(EXTRA_TB, "counter_sram_extra_tb.sv"))]
    if os.path.exists(my_tb):
        tbs.insert(0, ("your testbench", my_tb))
    sim.prefetch([(d, my_tb, SRAM_PORTS) for _, d in variants]
                 + [(d, tb, SRAM_PORTS) for d in (my_design, golden) for _, tb in tbs])
    if os.path.exists(my_tb):
        gold = check_tb_catches_bugs(rep, sim, my_tb, golden, variants, SRAM_PORTS, "your counter-SRAM testbench")
        if gold is None:
            tbs = tbs[1:]          # already reported; check the design with the other testbenches
        else:
            gaps = sram_coverage(gold)
            if gaps:
                rep.bad("your counter-SRAM testbench doesn't write and read every slot", "\n".join(gaps))
            else:
                rep.ok("your counter-SRAM testbench writes all 16 slots and reads them all back")
    if os.path.exists(my_design):
        check_design_matches_golden(rep, sim, my_design, golden, tbs, SRAM_PORTS, "your fixed counter-SRAM")

    rep.section("Write-up")
    check_writeup(rep, os.path.join(folder, "WRITEUP.md"),
                  os.path.join(v, "submission-template", "WRITEUP.md"))


# ====================================================================== Block 3
def simple_yaml(path):
    """Read `KEY: value` lines. Enough for config.yaml, and works without PyYAML."""
    try:
        import yaml  # noqa: PLC0415
        data = yaml.safe_load(read_text(path))
        return data if isinstance(data, dict) else None
    except ImportError:
        pass
    except Exception:  # noqa: BLE001
        return None
    data = {}
    for line in read_text(path).splitlines():
        line = line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if not m:
            return None
        val = m.group(2).strip()
        try:
            val = float(val) if "." in val else int(val)
        except ValueError:
            val = {"true": True, "false": False}.get(val.lower(), val)
        data[m.group(1)] = val
    return data


def gds_structures(path):
    """Names of every cell (structure) in a GDSII file, or None if it isn't GDSII."""
    names = []
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 6 or data[2:4] != b"\x00\x02":      # first record must be HEADER
        return None
    i = 0
    while i + 4 <= len(data):
        length = int.from_bytes(data[i:i + 2], "big")
        if length < 4:
            break
        rtype = data[i + 2]
        if rtype == 0x06:                                 # STRNAME
            names.append(data[i + 4:i + length].rstrip(b"\x00").decode("ascii", "ignore"))
        if rtype == 0x04:                                 # ENDLIB
            break
        i += length
    return names


def parse_metrics(path):
    """Return {run_name: {row_label: cell}} from the metrics.md table."""
    rows = [l.strip() for l in read_text(path).splitlines() if l.strip().startswith("|")]
    if len(rows) < 3:
        return None
    cells = lambda l: [c.strip() for c in l.strip("|").split("|")]  # noqa: E731
    header = cells(rows[0])
    runs = {h: {} for h in header[1:] if h}
    for line in rows[2:]:
        c = cells(line)
        for h, val in zip(header[1:], c[1:]):
            if h in runs:
                runs[h][c[0]] = val
    return runs


def numbers(cell):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", cell or "")]


def run_passes(table):
    """Must-pass checks for one run column. Returns (passed, reasons)."""
    reasons = []
    drc = [(k, v) for k, v in table.items() if "drc" in k.lower()]
    lvs = [(k, v) for k, v in table.items() if "lvs" in k.lower()]
    wns = [(k, v) for k, v in table.items() if "wns" in k.lower() or "worst slack" in k.lower()]
    if not drc or not lvs or not wns:
        return False, ["couldn't find the DRC, LVS, and WNS rows"]
    for k, v in drc + lvs:
        n = numbers(v)
        if not n:
            reasons.append(f"'{k}' is empty")
        elif any(x != 0 for x in n):
            reasons.append(f"'{k}' is {v}, needs to be 0")
    n = numbers(wns[0][1])
    if not n:
        reasons.append("WNS is empty")
    elif n[0] < 0:
        reasons.append(f"WNS is {wns[0][1]}, needs to be zero or positive")
    return not reasons, reasons


def check_block3(rep, folder, sim):
    rep.section("Files")
    names = ["src/counter_sram.sv", "config.yaml", "counter_sram.gds", "layout.png",
             "layout-zoom.png", "metrics.md", "WRITEUP.md"]
    require_files(rep, folder, names)
    for img in ("layout.png", "layout-zoom.png"):
        check_image(rep, os.path.join(folder, img), img)
    if os.path.isdir(os.path.join(folder, "runs")):
        rep.bad("the `runs/` folder is in your pull request", "Remove it. Lesson 6 explains why.")

    rep.section("Design")
    v = os.path.join(REPO, "verification")
    design = os.path.join(folder, "src", "counter_sram.sv")
    if os.path.exists(design):
        golden = os.path.join(v, "golden_counter_sram/counter_sram_design/counter_sram.sv")
        tbs = [("the golden testbench", os.path.join(v, "golden_counter_sram/testbench/counter_sram_tb.sv")),
               ("extra random inputs", os.path.join(EXTRA_TB, "counter_sram_extra_tb.sv"))]
        sim.prefetch([(d, tb, SRAM_PORTS) for d in (design, golden) for _, tb in tbs])
        if not check_design_matches_golden(rep, sim, design, golden, tbs, SRAM_PORTS,
                                           "`src/counter_sram.sv`"):
            rep.note("You hardened a design that still has a bug in it. Fix it, then run the flow again.")

    rep.section("Config")
    cfg_path = os.path.join(folder, "config.yaml")
    if os.path.exists(cfg_path):
        cfg = simple_yaml(cfg_path)
        if cfg is None:
            rep.bad("`config.yaml` can't be read", "Each line should be `NAME: value`, with a space after the colon.")
        else:
            good = True
            if cfg.get("DESIGN_NAME") != "counter_sram":
                rep.bad(f"DESIGN_NAME is `{cfg.get('DESIGN_NAME')}`, should be `counter_sram`")
                good = False
            files = cfg.get("VERILOG_FILES")
            files = " ".join(files) if isinstance(files, list) else str(files)
            if "src/counter_sram.sv" not in files:
                rep.bad(f"VERILOG_FILES is `{files}`, should point at `dir::src/counter_sram.sv`")
                good = False
            if not isinstance(cfg.get("CLOCK_PERIOD"), (int, float)):
                rep.bad("CLOCK_PERIOD is missing or isn't a number")
                good = False
            if good:
                rep.ok(f"`config.yaml` looks right (CLOCK_PERIOD {cfg['CLOCK_PERIOD']} ns, "
                       f"FP_CORE_UTIL {cfg.get('FP_CORE_UTIL', 'default')})")

    rep.section("Layout")
    gds = os.path.join(folder, "counter_sram.gds")
    if os.path.exists(gds):
        size = os.path.getsize(gds)
        cells = gds_structures(gds)
        if cells is None:
            rep.bad("`counter_sram.gds` isn't a GDS file",
                    "Copy it from `runs/<your run>/final/gds/counter_sram.gds` (Lesson 6, Step 1).")
        elif "counter_sram" not in cells:
            rep.bad("`counter_sram.gds` has no `counter_sram` cell in it",
                    "It may be the tutorial's layout. Copy yours from `runs/<your run>/final/gds/`.")
        else:
            rep.ok(f"`counter_sram.gds` is a real layout with a `counter_sram` cell "
                   f"({len(cells)} cells, {size / 1e6:.1f} MB)")
        if size > 50e6:
            rep.bad(f"`counter_sram.gds` is {size / 1e6:.0f} MB", "GitHub rejects files over 100 MB. Ask a lead.")

    rep.section("Metrics")
    met = os.path.join(folder, "metrics.md")
    if os.path.exists(met):
        runs = parse_metrics(met)
        if not runs:
            rep.bad("couldn't read the table in `metrics.md`", "Use the table from Lesson 3, Step 1.")
        else:
            if len(runs) < 2:
                rep.bad("`metrics.md` only has one run", "Lesson 5 adds a second column for the changed run.")
            results = {name: run_passes(t) for name, t in runs.items()}
            passing = [n for n, (p, _) in results.items() if p]
            if passing:
                rep.ok(f"must-pass numbers are met in: {', '.join(passing)}")
            else:
                rep.bad("no run in `metrics.md` has 0 DRC, 0 LVS, and WNS zero or positive",
                        "\n".join(f"{n}: {'; '.join(r)}" for n, (_, r) in results.items()))

    rep.section("Write-up")
    text = check_writeup(rep, os.path.join(folder, "WRITEUP.md"),
                         os.path.join(REPO, "physical-design", "submission-template", "WRITEUP.md"))
    if text:
        empty = []
        for stage in ("Synthesis", "Floorplan", "Placement", "Clock tree synthesis", "Routing", "Signoff"):
            m = re.search(r"\*\*" + re.escape(stage) + r":\*\*(.*?)(?=\*\*[A-Z][A-Za-z ]+:\*\*|\n#|\Z)",
                          text, re.DOTALL)
            if not m or len(m.group(1).split()) < 5:
                empty.append(stage)
        if empty:
            rep.bad("some of the six stages have no explanation", "Fill in: " + ", ".join(empty))
        else:
            rep.ok("all six stages are explained")


# ====================================================================== pull request
def check_pull_request(rep, changed, author):
    """Return the one submission folder this pull request is about, or None."""
    folders, outside = set(), []
    for path in changed:
        parts = path.split("/")
        if len(parts) >= 4 and parts[0] == "submissions" and parts[1] in BLOCKS:
            folders.add("/".join(parts[:3]))
        elif path:
            outside.append(path)

    rep.section("Pull request")
    if outside:
        rep.bad(f"this pull request changes {len(outside)} file(s) outside your submission folder",
                "\n".join(outside[:10]) + ("\n..." if len(outside) > 10 else "")
                + "\nOnly add your own folder: `git add submissions/<block>/<your-username>`. "
                "Ask in the GroupMe if you're not sure how to undo this.")
    if len(folders) > 1:
        rep.bad("this pull request changes more than one submission folder",
                "\n".join(sorted(folders)) + "\nEach block gets its own branch and pull request.")
    if len(folders) == 1:
        folder = folders.pop()
        user = folder.split("/")[2]
        if author and user.lower() != author.lower():
            rep.bad(f"the folder is named `{user}`, but your GitHub username is `{author}`",
                    "Name the folder exactly after your GitHub username.")
        if not outside:
            rep.ok(f"only changes `{folder}/`")
        return folder
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", help="your submission folder, e.g. submissions/verification/jsmith")
    ap.add_argument("--changed", help="(GitHub) file listing the paths this pull request changes")
    ap.add_argument("--author", help="(GitHub) the pull request author's username")
    args = ap.parse_args()

    rep = Report()
    if args.changed:
        changed = [l.strip() for l in read_text(args.changed).splitlines() if l.strip()]
        folder = check_pull_request(rep, changed, args.author)
        if folder is None and not any(c.startswith("submissions/") for c in changed):
            print("This pull request doesn't touch submissions/. Nothing to check.")
            return 0
    else:
        if not args.folder:
            ap.error("give your submission folder, e.g. submissions/verification/YOUR-GITHUB-USERNAME")
        folder = os.path.relpath(os.path.abspath(args.folder), REPO)

    heading = "Submission check"
    sim = Sim()
    try:
        if folder:
            block = folder.split("/")[1] if folder.count("/") >= 2 else None
            path = os.path.join(REPO, folder)
            heading = f"Submission check: `{folder}`"
            if not os.path.isdir(path):
                rep.bad(f"`{folder}` doesn't exist")
            elif block == "digital-design":
                check_block1(rep, path)
            elif block == "verification":
                check_block2(rep, path, sim)
            elif block == "physical-design":
                check_block3(rep, path, sim)
            else:
                rep.bad(f"`{folder}` isn't a submission folder",
                        "It should look like submissions/<block>/<your-github-username>.")
    except RuntimeError as e:
        rep.bad(str(e))
    finally:
        sim.cleanup()

    print(f"\n{heading}")
    rep.print_terminal()
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(rep.markdown(heading.replace("`", "")))
    return 1 if rep.problems else 0


if __name__ == "__main__":
    sys.exit(main())
