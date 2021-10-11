#!/bin/bash
rm *_removed.ipynb

for i in *ipynb; do
	python remove_output.py $i  || exit 1
done

for i in *_removed.ipynb; do
	mv $i ${i//_removed}
done

for i in *.ipynb; do
	jupyter nbconvert --to notebook $i &
done
wait

mv *nbconvert.ipynb rendered_notebooks
