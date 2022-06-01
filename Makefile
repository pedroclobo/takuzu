all:: tests

tests:: 
	@$(MAKE) $(MFLAGS) -C tests

clean::
	(rm -rf src/__pycache__ && rm -f tests/*.diff)
