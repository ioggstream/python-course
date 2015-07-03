#
# Makefile for creating beamer tex file
#  from markdown via pandoc
#
SOURCES=$(wildcard *.md)
TEX=$(SOURCES:.md=.md.tex)


sources: $(TEX)

test: sources
	pdflatex --shell-escape -interaction=nonstopmode test.tex

main: sources
	pdflatex --shell-escape -interaction=nonstopmode main.tex


debug: sources
	pdflatex --shell-escape main.tex


%.md.tex: %.md
	pandoc $< -f markdown --highlight-style=kate  --no-tex-ligatures -t beamer -o $@
	sed -i 's/{frame}\(\[fragile\]\)\?/{pyframe}/g; s/verbatim/bashcode/g; s/Shaded/mdframed/g; s/\\pythonbegin/\\begin{pycode*}/g; s/\\pythonend/\end{pycode*}/g; ' \
	 $@


clean:
	rm -vf *.aux *.dvi *.log *.nav *.out \
	    *.snm *.toc *.vrb *.idx *.ind *.upa \
	    *.md.tex *.tmp *.stderr \
	    main.pdf main.sh


