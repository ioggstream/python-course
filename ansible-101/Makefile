#
# To run the environment, use
#
# # make course
#
.PHONY: course

MAIN_IP = $(shell ip -4 -o a s scope global | awk -F'[/ ]+' '{print $$4; exit} ')

clean:
	rm *.pyc __pycache__ -fr
	find notebooks -name '*_removed.nbconvert.ipynb' -delete
	find notebooks -name '*_removed.ipynb' -delete

clean-other:
	docker-compose kill bastion web 
	docker-compose rm -vf bastion web 

test:
	docker exec -ti ansible101_dev_1 bash -c ' (cd /notebooks; ./cleanup.sh ) ' 

dev:
	docker-compose scale dev=1 web=2 bastion=1
	docker-compose logs dev | grep token | sed -e "s/0.0.0.0/$(MAIN_IP)/g"

course:
	docker-compose scale course=1 web=2 bastion=1
	docker-compose logs course | grep token | sed -e "s/0.0.0.0/$(MAIN_IP)/g"

