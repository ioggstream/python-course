FILES=$(wildcard *.md)
BOOKS = $(patsubst %.md,notebooks/%.ipynb,$(FILES))


all: $(BOOKS)
	@echo $(BOOKS)

clean:
	rm -rf notebooks/*.ipynb

notebooks/%.ipynb: %.md

	notedown --to notebook $^ > $@

run: all
	jupyter notebook notebooks
