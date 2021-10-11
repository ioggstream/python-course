#
# Load styles and images from texinputs using
#  the TEXINPUTS variable.
#  *RESPECT THE ORDER*
#   - first current directory .
#   - ../texinputs
#   - other paths
#
export TEXINPUTS = .:../texinputs/:./images/:/tmp/tox:
include ../texinputs/Makefile

training: 99-training.md.tex
	pdflatex --shell-escape -interaction=nonstopmode training.tex
