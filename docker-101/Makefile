FILES=$(wildcard *.md)
BOOKS = $(patsubst %.md,notebooks/%.ipynb,$(FILES))


all: $(BOOKS)
	@echo $(BOOKS)
	cp Dockerfile notebooks/Dockerfile

notebooks/%.ipynb: %.md
	notedown --to notebook $^ > $@
