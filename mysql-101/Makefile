export TEXINPUTS=:.:../texinputs
include ../texinputs/Makefile

# Create a revealjs image. You can view it with
#   docker run -v $PWD:/revealjs/slides -p8000:8000 --rm -ti amouat/revealjs
#   firefox http://localhost:8000/

revealjs:
	rm slides.md
	cat lesson*.md > slides.md
	sed -i 's/^[#+]/\n\n---\n\n\n&/' slides.md
