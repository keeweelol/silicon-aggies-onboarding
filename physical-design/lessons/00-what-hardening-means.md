# Lesson 0: What "hardening" means

**Hardening** a design means turning your Verilog into a physical layout that a factory can
build. Nobody does this by hand anymore. A chain of tools does it, each one taking the
previous tool's output and adding more physical detail. That chain is called the **flow**.
The flow we use is called **LibreLane**.

This lesson walks through the six stages of the flow. You don't run anything yet. These six
names are what the whole industry calls these steps, so they're worth learning. They come up
in internship interviews.

---

## An analogy first

Think about building a house from a description.

1. You start with a description: "three bedrooms, two bathrooms, a kitchen." (That's your
   Verilog.)
2. An architect turns it into a list of actual parts: these doors, these windows, these
   pipes. (**Synthesis**)
3. You pick the size of the lot, where the driveway goes, and where power comes in from the
   street. (**Floorplan**)
4. You decide exactly where each room and appliance sits. (**Placement**)
5. You make sure the water heater reaches every faucet at the same pressure. (**Clock tree**)
6. You run all the wires and pipes between everything. (**Routing**)
7. An inspector checks everything against building code before anyone moves in. (**Signoff**)

## The six stages

| Stage | Tool | What it does | What comes out |
|---|---|---|---|
| **Synthesis** | Yosys | Turns your Verilog into a list of real standard cells: specific AND gates, flip-flops, and buffers from the sky130 library that the factory knows how to build | A gate-level netlist |
| **Floorplan** | OpenROAD | Decides how big the chip is, where the input and output pins go, and lays down the grid of power wires | Chip size and power grid |
| **Placement** | OpenROAD | Gives every cell an exact x, y position, lined up in rows | Placed cells |
| **Clock tree synthesis (CTS)** | OpenROAD | Builds a tree of buffers that carries the clock to every flip-flop so the edge arrives everywhere at nearly the same time | Clock buffers added |
| **Routing** | OpenROAD | Draws the metal wires that connect everything, using up to five stacked layers of metal | Fully wired design |
| **Signoff** | OpenROAD, Magic, KLayout, Netgen | Checks that the design is fast enough (timing), follows the factory's rules (DRC), and that the layout matches the netlist (LVS) | Reports, and the final `.gds` |

A few words from that table:

- **Standard cell:** a small, pre-designed building block like an AND gate or a flip-flop.
  The factory provides a library of them. Synthesis builds your design out of these.
- **Netlist:** a list of cells and which wires connect them. No positions yet, just
  connections.
- **sky130:** the manufacturing process we use, from SkyWater Technology. Its design files
  (the **PDK**, or process design kit) are open source.
- **DRC (design rule check):** the factory's rules about how close wires can be, how wide
  they have to be, and so on. Zero DRC errors means the factory can build it.
- **LVS (layout versus schematic):** a check that the drawn layout is the same
  circuit as the netlist. "LVS clean" means they match.
- **Timing:** whether signals get where they need to go before the next clock edge. You'll
  see this as **slack** in Lesson 3.

In your write-up at the end of the block, you'll explain these six stages in your own words,
using numbers from your own run.

---

**Next:** [Lesson 1: Run the tutorial](01-run-the-tutorial.md).
