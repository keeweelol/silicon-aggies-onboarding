#!/usr/bin/env bash
# Checks that the tools for each block are installed.
# Run it from the repo folder:   bash setup/check.sh

check() {
    # $1 = what to show, $2 = command to run, $3 = which block needs it
    if out=$(eval "$2" 2>&1) && [ -n "$out" ]; then
        printf "  ok       %-10s %s\n" "$1" "$(echo "$out" | head -1)"
    else
        printf "  MISSING  %-10s (needed for %s)\n" "$1" "$3"
    fi
}

echo ""
echo "Checking your tools..."
echo ""
check "git"       "git --version"                    "everything"
check "gh"        "gh --version"                     "turning in work"
check "iverilog"  "iverilog -V 2>&1 | head -1"       "Block 1"
check "gtkwave"   "gtkwave --version"                "Blocks 1 and 2"
check "python3"   "python3 --version"                "Block 1"
check "make"      "make --version"                   "Block 1"
check "verilator" "verilator --version"              "Block 2"
check "g++"       "g++ --version"                    "Block 2"
check "nix"       "nix --version"                    "Block 3"
echo ""

# Block 2 needs Verilator 5 or newer.
if command -v verilator >/dev/null 2>&1; then
    major=$(verilator --version | awk '{print $2}' | cut -d. -f1)
    if [ "$major" -lt 5 ] 2>/dev/null; then
        echo "  PROBLEM: your Verilator is version $major. Block 2 needs 5 or newer."
        echo "           See Part C of setup/README.md."
        echo ""
    fi
fi

# gh has to be logged in, or git push will fail later.
if command -v gh >/dev/null 2>&1 && ! gh auth status >/dev/null 2>&1; then
    echo "  PROBLEM: gh is installed but you are not logged in. Run: gh auth login"
    echo ""
fi
