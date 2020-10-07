SOURCES=$(shell find . -name "*.tex")
TARGETS=$(SOURCES:.tex=.pdf)
BIB=$(shell find . -name ".bib")
DATA=example.csv by-classes.csv
.PHONY: all

all: $(DATA) $(TARGETS)

$(TARGETS): $(SOURCES) $(BIB)

%.pdf: %.tex
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@biber $*
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@rm -f $*.log $*.aux $*.ilg $*.ind $*.toc $*.bbl $*.blg $*.out $*.asc $*.asc $*.run.xml $*.bcf

%.csv: scripts/make_%.py
	@python3 scripts/make_$*.py

clean:
	@rm *.pdf
	@rm *.csv
