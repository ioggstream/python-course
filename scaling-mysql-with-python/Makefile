#
# Load styles and images from texinputs using
#  the TEXINPUTS variable
#
export TEXINPUTS = ../texinputs/:.:

default:
	make all

check:
	lacheck babel.tex | egrep -v "Dots should be |Whitespace before punctation|to (begin|end) quotation|possible unwanted space"

all:	
	pdflatex --shell-escape -interaction=nonstopmode main_*.tex

allsilent:
	nohup pdflatex --shell-escape -interaction=nonstopmode main_*.tex > /dev/null
	tail main_*.log
test:
	pdflatex --shell-escape -interaction=nonstopmode test.tex

testdebug:
	pdflatex --shell-escape test.tex

pytest:
	rm snippet.tex snippet.pdf; true
	pygmentize -o snippet.tex -f latex -l python -P mathescape -F tokenmerge -O full=true,escapeinside="||" snippet.py
	pdflatex --shell-escape snippet.tex

debug:
	pdflatex --shell-escape main_*.tex

backup:
	zip -r backup-$(basename $PWD).zip *.tex Makefile *.png

clean:
	rm -vf *.aux *.dvi *.log *.nav *.out *.snm *.toc *.vrb *.idx *.ind *.upa backup.zip

distclean:
	make clean
	rm -vf main_*.pdf

listpdf:
	egrep -o '[a-z_]+.pdf' *.tex
