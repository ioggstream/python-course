FILES = $(wildcard *.md)
BOOKS = $(patsubst %.md,notebooks/%.ipynb,$(FILES))


all: $(BOOKS) notebooks/index.md
	@echo $(BOOKS)

notebooks/index.md: $(BOOKS)
	echo "# Index\n\n" > $@
	for file in $(BOOKS); do echo >> $@ \
			"- [$$file](https://jupyter.org/try-jupyter/lab/?fromURL=https://raw.githubusercontent.com/ioggstream/python-course/main/python-high-school/$$file)" ; done
clean:
	rm -rf notebooks/*.ipynb notebooks/index.md

notebooks/%.ipynb: %.md
	notedown --to notebook $^ > $@

run: all
	jupyter notebook notebooks
