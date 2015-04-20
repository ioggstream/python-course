#
# Makefile for creating beamer tex file 
#  from markdown via pandoc
#
SOURCES=$(wildcard *.md)
TEX=$(SOURCES:.md=.md.tex)


sources: $(TEX)

main: sources
	pdflatex --shell-escape main.tex
	
	
%.md.tex: %.md
	pandoc $< -f markdown -t beamer -o $@

clean:
	rm -vf *.aux *.dvi *.log *.nav *.out \
	    *.snm *.toc *.vrb *.idx *.ind *.upa \
	    *.md.tex *.tmp 


