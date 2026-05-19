FILES=$(wildcard [0-9]*.md)
BOOKS = $(patsubst %.md,notebooks/%.ipynb,$(FILES))
SLIDES = $(patsubst %.ipynb,%.slides.html,$(BOOKS))


all: $(SLIDES)
	@echo $(SLIDES)

notebooks/%.ipynb: %.md

	notedown --to notebook $^ > $@

%.slides.html: %.ipynb

	jupyter nbconvert --to slides $<

clean:
	rm -f notebooks/*.ipynb notebooks/*.slides.html
