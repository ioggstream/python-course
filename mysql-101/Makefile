export TEXINPUTS=:.:../texinputs
include ../texinputs/Makefile

# Create a revealjs image. You can view it with
#   docker run -v $PWD:/revealjs/slides -p8000:8000 --rm -ti amouat/revealjs
#   firefox http://localhost:8000/

revealjs:
	rm slides.md
	cat lesson*.md > slides.md
	sed -i 's/^[#+]/\n\n---\n\n\n&/' slides.md

.PHONY: course

MAIN_IP = $(shell ip -4 -o a s scope global | awk -F'[/ ]+' '{print $$4; exit} ')
EXTERNAL_COURSES = 


course: .prepare
	docker-compose scale centos=3 mysql=3 & 
	bash 2>/dev/null ~/.bashrc
	wait
	
.prepare:
	echo "done"

