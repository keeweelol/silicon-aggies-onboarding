import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


async def step(dut, n=1):
    """Advance n clock edges, then wait 1ns so the outputs have settled.

    Without that settle you are sampling the wires at the exact instant the
    flip-flops are updating, and you will read the OLD value. This is the single
    most common cocotb mistake. Always look after things have stopped moving.
    """
    await ClockCycles(dut.clk, n)
    await Timer(1, unit="ns")


def set_ctrl(dut, en=0, load=0):
    """uio_in[0] = enable, uio_in[1] = load."""
    dut.uio_in.value = (load << 1) | en


async def setup(dut):
    """Start the clock, apply reset, leave the counter idle at 0."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await step(dut, 3)
    dut.rst_n.value = 1
    await step(dut, 1)


def count(dut):
    return int(dut.uo_out.value)


@cocotb.test()
async def test_reset(dut):
    await setup(dut)
    assert count(dut) == 0, f"after reset count should be 0, got {count(dut)}"


@cocotb.test()
async def test_counts_up(dut):
    await setup(dut)
    set_ctrl(dut, en=1)
    for expected in range(1, 11):
        await step(dut)
        assert count(dut) == expected, f"expected {expected}, got {count(dut)}"


@cocotb.test()
async def test_holds_when_disabled(dut):
    await setup(dut)
    set_ctrl(dut, en=1)
    await step(dut, 5)
    before = count(dut)
    set_ctrl(dut, en=0)
    await step(dut, 10)
    assert count(dut) == before, f"counter moved while disabled: {before} -> {count(dut)}"


@cocotb.test()
async def test_rollover(dut):
    await setup(dut)
    dut.ui_in.value = 254
    set_ctrl(dut, load=1)
    await step(dut)
    assert count(dut) == 254, f"load failed: expected 254, got {count(dut)}"
    set_ctrl(dut, en=1)
    await step(dut)
    assert count(dut) == 255, f"expected 255, got {count(dut)}"
    await step(dut)
    assert count(dut) == 0, f"255 + 1 should wrap to 0, got {count(dut)}"
