OBJ=babel.pdf test.pdf
export TEXINPUTS = ../texinputs/:.:

default:
	make all

check:
	lacheck babel.tex | egrep -v "Dots should be |Whitespace before punctation|to (begin|end) quotation|possible unwanted space"

all:
	pdflatex --shell-escape -interaction=nonstopmode babel.tex

stat:
	pdflatex --shell-escape -interaction=nonstopmode stat101.tex

allsilent:
	nohup pdflatex --shell-escape -interaction=nonstopmode babel.tex > /dev/null
	tail babel.log
test:
	pdflatex --shell-escape -interaction=nonstopmode test.tex
testdebug:
	pdflatex --shell-escape test.tex
pytest:
	rm snippet.tex snippet.pdf; true
	pygmentize -o snippet.tex -f latex -l python -P mathescape -F tokenmerge -O full=true,escapeinside="||" snippet.py
	pdflatex --shell-escape snippet.tex

debug:
	pdflatex --shell-escape babel.tex

backup:
	zip -r ep14-python-sysadmin.zip *.tex Makefile *.png

clean:
	rm -vf *.aux *.dvi *.log *.nav *.out *.snm *.toc *.vrb *.idx *.ind *.upa ep14-python-sysadmin.zip

distclean:
	make clean
	rm -vf babel.pdf test.pdf

listpdf:
	egrep -o '[a-z_]+.pdf' *.tex
