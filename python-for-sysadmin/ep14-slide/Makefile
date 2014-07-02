all:
	pdflatex --shell-escape -interaction=nonstopmode babel.tex

test:
	pdflatex --shell-escape -interaction=nonstopmode test.tex

debug:
	pdflatex --shell-escape babel.tex

backup:
	zip -r ep14-python-sysadmin.zip *.tex Makefile *.png

clean:
	rm -vf *.aux *.dvi *.log *.nav *.out *.snm *.toc *.vrb 
