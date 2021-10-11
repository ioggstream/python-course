#
# To run the environment, use
#
# # make course
#
.PHONY: course
.EXPORT_ALL_VARIABLES:

MAIN_IP = $(shell ip -4 -o a s scope global | awk -F'[/ ]+' '{print $$4; exit} ')
EXTERNAL_COURSES =


course: .prepare .EXPORT_ALL_VARIABLES
	docker-compose scale course=1 editor=1
	docker-compose logs course | grep token | sed -e "s/0.0.0.0/$(MAIN_IP)/g"  | sed -e "s/(.* or 127.0.0.1)/$(MAIN_IP)/g"

clean:
	rm *.pyc __pycache__ -fr
	find notebooks -name '*_removed.nbconvert.ipynb' -delete
	find notebooks -name '*_removed.ipynb' -delete
	find notebooks -name '.*' -prune -o -name \*.yml -type f -exec sed -i 's/[[:space:]]*$$//' {} \;
	# find notebooks -name \*.yml -type f -exec ansible-lint {} \;
	find notebooks -name '.*' -prune -o  -name '*.ipynb' -exec  nbstripout {} \;
	# $(foreach dpath, $(EXTERNAL_COURSES), rm -f notebooks/$(dpath)/*.ipynb; )

clean-other:
	docker-compose kill editor dev
	docker-compose rm -vf editor dev

test:
	docker exec -ti connexion101_dev_1 bash -c ' (cd /notebooks; ./cleanup.sh ) '

dev: .prepare .EXPORT_ALL_VARIABLES
	docker-compose scale dev=1 editor=1
	docker-compose logs dev | grep token | sed -e "s/0.0.0.0/$(MAIN_IP)/g" | sed -e "s/(.* or 127.0.0.1)/$(MAIN_IP)/g"

.prepare:
	# build all EXTERNAL_COURSES
	$(foreach dpath, $(EXTERNAL_COURSES), cd ../$(dpath); ! test -f Makefile || make; )
	$(foreach dpath, $(EXTERNAL_COURSES), mkdir -p notebooks/rendered_notebooks/$(dpath); rsync -var  ../$(dpath)/notebooks/ notebooks/rendered_notebooks/$(dpath); )
	cp  ../python-for-sysadmin/requirements.txt .
