SOURCES=$(shell find . -name "*.tex")
TARGETS=$(SOURCES:.tex=.pdf)
BIB=$(shell find . -name ".bib")
DATA=example.csv by-classes.csv by-actors.csv by-duration.csv by-agents.csv
IMG=by-collision.png by-camera.png example_gui_tool.png
.PHONY: all

all: $(DATA) $(IMG) $(TARGETS)

$(TARGETS): $(SOURCES) $(BIB)

%.pdf: %.tex
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@biber $*
	@pdflatex -interaction nonstopmode -halt-on-error -file-line-error $*
	@rm -f $*.log $*.aux $*.ilg $*.ind $*.toc $*.bbl $*.blg $*.out $*.asc $*.asc $*.run.xml $*.bcf

%.csv: scripts/make_%.py
	@python3 scripts/make_$*.py

%.png: scripts/make_%.py
	@python3 scripts/make_$*.py

clean:
	@rm *.pdf
	@rm *.csv
