FILE = main

PRINTER = lp
UNAME = $(shell uname)
ifeq ($(UNAME),Linux)
	OPEN_COMMAND = evince
endif
ifeq ($(UNAME),Darwin)
	OPEN_COMMAND = open
endif

all:	$(FILE).tex
	pdflatex $(FILE)
	pdflatex $(FILE)

clean:
	rm -f $(FILE).ps $(FILE).pdf $(FILE).log $(FILE).dvi $(FILE).bbl $(FILE).blg $(FILE).aux
	rm -f *.toc
	rm -f *.out
	rm -f *~
	rm -f *.bak
	rm -f *.backup
	rm -f *.log

bib:	$(FILE).tex
	pdflatex $(FILE)
	pdflatex $(FILE)
	bibtex $(FILE)

p:	
	lpr -P$(PRINTER) $(FILE).ps; 
	lpq -P$(PRINTER)

dist:
	tar cfj ../$(FILE)-`date +%F`.tar.bz2 .
