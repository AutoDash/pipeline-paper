SOURCES=$(shell find . -name "*.tex")
TARGETS=$(SOURCES:.tex=.pdf)
BIB=$(shell find . -name ".bib")

.PHONY: all

all: $(TARGETS)

$(TARGETS): $(SOURCES) $(BIB)

%.pdf: %.tex
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@biber $*
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@rm -f $*.log $*.aux $*.ilg $*.ind $*.toc $*.bbl $*.blg $*.out $*.asc $*.asc $*.run.xml $*.bcf

clean:
	@rm *.pdf
