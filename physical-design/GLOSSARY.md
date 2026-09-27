# Glossary (Block 3)

New terms from this block, in plain language. For earlier terms, see the
[Block 1](../digital-design/GLOSSARY.md) and [Block 2](../verification/GLOSSARY.md)
glossaries.

---

**Antenna violation:** a long wire that could collect enough static charge during
manufacturing to damage a transistor. The flow usually fixes these by adding small diodes.

**Cell library:** the set of standard cells a factory provides for a process. Ours is
`sky130_fd_sc_hd`, which is why every cell name starts with that.

**Clock tree synthesis (CTS):** the flow stage that builds a tree of buffers to carry the
clock to every flip-flop at nearly the same moment.

**Config file:** `config.yaml`, the file that tells LibreLane which design to build and how.

**Die area:** the size of the whole chip, in square micrometers (µm²).

**DRC (design rule check):** checks that the layout follows the factory's rules about wire
widths, spacing, and so on. You need zero DRC errors.

**Filler and tap cells:** cells with no logic in them. The flow adds them to fill gaps in
the rows and connect the rows to power.

**Floorplan:** the flow stage that sets the chip size, places the input and output pins,
and lays down the power grid.

**Flow:** the chain of tools that turns Verilog into a layout. Ours is LibreLane.

**GDS:** the file format for a finished chip layout. It's what factories accept and what we
submit to Tiny Tapeout.

**Hardening:** turning a design into a physical layout.

**KLayout:** the program you use to look at a GDS file.

**Layer:** one kind of material in the chip, like a metal wiring level or the transistor
gates. Layouts are stacks of layers.

**LibreLane:** the open-source flow we use. It runs Yosys, OpenROAD, Magic, KLayout, and
Netgen for you, in order.

**LVS (layout versus schematic):** checks that the drawn layout is the same circuit as the
netlist. "LVS clean" means zero errors.

**Macro:** a large, pre-built block you drop into a design, like the SRAM blocks in the
tutorial.

**met1 to met5:** the five metal wiring layers in sky130, from lowest to highest.

**Metrics:** the numbers the flow measures, like area, slack, and error counts. They're
collected in `final/metrics.csv`.

**Netlist:** a list of cells and the wires connecting them, without positions.

**Nix:** the tool that installs LibreLane with exactly the same versions for everyone.
`nix-shell` starts the LibreLane environment.

**PDK (process design kit):** the files a factory provides describing its process: the cell
library, the design rules, the layers. We use sky130.

**PDN (power distribution network):** the grid of power wires across the chip.

**Placement:** the flow stage that gives every cell an exact position.

**Routing:** the flow stage that draws the metal wires between cells.

**Run tag:** the name you give a run with `--run-tag`. Results go in `runs/<tag>`.

**Signoff:** the final checks (timing, DRC, LVS) before a design is ready to manufacture.

**sky130:** the open-source 130 nm manufacturing process from SkyWater Technology.

**Slack:** how much spare time a signal has before the next clock edge. Positive is good.
Negative means the path is too slow.

**Standard cell:** a small, pre-designed building block like an AND gate or a flip-flop.

**STA (static timing analysis):** the check that measures slack on every path.

**Synthesis:** the flow stage that turns Verilog into a netlist of standard cells.

**TNS (total negative slack):** all the negative slack in the design added up. Zero means
no path is too slow.

**Utilization:** the percent of the core area filled with cells. Set with `FP_CORE_UTIL`.

**WNS (worst negative slack):** the slack on the slowest path. Zero or positive means timing
is met.

**Yosys:** the synthesis tool.
