FILES=$(wildcard *.md)
BOOKS = $(patsubst %.md,notebooks/%.ipynb,$(FILES))
SLIDES = $(patsubst %.ipynb,%.html,$(BOOKS))


all: $(BOOKS)
	@echo $(BOOKS) $(SLIDES)

notebooks/%.ipynb: %.md

	notedown --to notebook $^ > $@

%.html: %.ipynb

	jupyter nbconvert --to slides $^ --post serve

clean:
	rm notebooks/*.ipynb -f
