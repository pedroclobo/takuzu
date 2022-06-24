all:: relatorio

tests::
	@$(MAKE) $(MFLAGS) -C tests

relatorio::
	(cd docs && pdflatex relatorio.tex)

clean::
	(rm -rf src/__pycache__ && rm -f tests/*.diff && rm -f docs/relatorio.pdf && find . | egrep '*.aux|*.log|*.out' | grep -v ".git" | grep -v "tests" | xargs \rm -f)
