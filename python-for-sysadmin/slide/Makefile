OBJ=babel.pdf test.pdf
export TEXINPUTS=:.:../../texinputs

default:
	make all

check:
	lacheck babel.tex | egrep -v "Dots should be |Whitespace before punctation|to (begin|end) quotation|possible unwanted space"

all:	
	pdflatex --shell-escape -interaction=nonstopmode babel.tex
	mv babel.pdf python-for-sysadmin-draft-2015.pdf

allsilent:
	nohup pdflatex --shell-escape -interaction=nonstopmode babel.tex > /dev/null
	tail babel.log

pytest:
	rm snippet.tex snippet.pdf; true
	pygmentize -o snippet.tex -f latex -l python -P mathescape -F tokenmerge -O full=true,escapeinside="||" snippet.py
	pdflatex --shell-escape snippet.tex

debug:
	pdflatex --shell-escape babel.tex

backup:
	zip -r backup-slide.zip *.tex Makefile *.png

clean:
	rm -vf *.aux *.dvi *.log *.nav *.out *.snm *.toc *.vrb *.idx *.ind *.upa backup-slide.zip

distclean:
	make clean
	rm -vf babel.pdf

listpdf:
	egrep -o '[a-z_]+\.pdf' *.tex
