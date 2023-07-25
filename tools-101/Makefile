#
# To run the environment, use
#
# # make course
#
# # or if you want override default value of EXTERNAL_COURSES, please use an environment variable
# # EXTERNAL_COURSES=git-101 make course
#
.PHONY: course

MAIN_IP = $(shell ip -4 -o a s scope global | awk -F'[/ ]+' '{print $$4; exit} ')

ifndef EXTERNAL_COURSES
EXTERNAL_COURSES = git-101 python-basic docker-101
endif


course: .prepare

clean:
	rm *.pyc __pycache__ -fr
	find notebooks -name '*_removed.nbconvert.ipynb' -delete
	find notebooks -name '*_removed.ipynb' -delete
	find notebooks -name \*.yml -type f -exec sed -i 's/[[:space:]]*$$//' {} \;
	# find notebooks -name \*.yml -type f -exec ansible-lint {} \;
	find notebooks -name '*.ipynb' -exec  nbstripout {} \;
	# $(foreach dpath, $(EXTERNAL_COURSES), rm -f notebooks/$(dpath)/*.ipynb; )
 
# clean-other:
# 	docker-compose kill bastion web
# 	docker-compose rm -vf bastion web
# 
# test:
# 	docker exec -ti tools101_dev_1 bash -c ' (cd /notebooks; ./cleanup.sh ) '
# 
# dev: .prepare
# 	docker-compose scale dev=1
# 	docker-compose logs dev | grep token | sed -e "s/0.0.0.0/$(MAIN_IP)/g" | sed -e "s/(sysadminpy or 127.0.0.1)/$(MAIN_IP)/g"
# 
.prepare:
	# build all EXTERNAL_COURSES
	$(foreach dpath, $(EXTERNAL_COURSES), cd ../$(dpath); ! test -f Makefile || make; )
	$(foreach dpath, $(EXTERNAL_COURSES), mkdir -p notebooks/rendered_notebooks/$(dpath); rsync -var  ../$(dpath)/notebooks/ notebooks/rendered_notebooks/$(dpath); )
	cp ../python-for-sysadmin/requirements.txt .
	make -f markdown.mak

run: course
	jupyter notebook notebooks