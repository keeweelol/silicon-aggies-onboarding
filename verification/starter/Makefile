SIM ?= icarus
TOPLEVEL_LANG ?= verilog

DUT ?= tt_um_counter.v
VERILOG_SOURCES += $(PWD)/$(DUT)

TOPLEVEL = tt_um_counter
MODULE   = test_counter

include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf sim_build results.xml dump.vcd
