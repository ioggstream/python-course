#
# Load styles and images from texinputs using
#  the TEXINPUTS variable
#
export TEXINPUTS = ../texinputs/:.:/tmp/tox:
CFLAGS=--shell-escape

default: all

check:
	lacheck main_*.tex | egrep -v "Dots should be |Whitespace before punctation|to (begin|end) quotation|possible unwanted space"

all: talk training

talk:
	pdflatex  $(CFLAGS) -interaction=nonstopmode main_scaling_mysql.tex

training:
	pdflatex $(CFLAGS) -interaction=nonstopmode main_training_mysql.tex
	mv main_training_mysql.pdf  orchestrating-mysql-with-python-and-docker.pdf

allsilent:
	nohup pdflatex --shell-escape -interaction=nonstopmode main_*.tex > /dev/null
	tail main_*.log

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

