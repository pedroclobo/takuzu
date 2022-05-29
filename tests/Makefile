.SUFFIXES: .in .out .diff
MAKEFLAGS += --no-print-directory
GREEN=$(shell tput setaf 2)
RED=$(shell tput setaf 1)
RESET=$(shell tput op)
OK="$(GREEN)$< PASSED$(RESET)"
KO="$(RED)$< FAILED$(RESET)"
EXE=python ../src/takuzu.py

all:: clean
	@$(MAKE) $(MFLAGS) `ls *.in | sed -e "s/in/diff/"`

.in.diff:
	@-$(EXE) < $< | diff - $*.out > $@
	@if [ `wc -l < $@` -eq 0 ]; then echo $(OK); else echo $(KO); fi;

clean::
	@rm -f *.diff
