clean:
	rm *.pyc __pycache__ -fr
	find notebooks -name '*_removed.nbconvert.ipynb' -delete
	find notebooks -name '*_removed.ipynb' -delete


test:
	docker exec -ti ansible101_dev_1 bash -c ' (cd /notebooks; 		for i in *.ipynb; do 	python remove_output.py \$i ; done ) ' 

dev:
	docker-compose scale dev=1 web=2 bastion=1
	docker-compose logs dev

