clean:
	rm *.pyc __pycache__ -fr
	find notebooks -name '*_removed.nbconvert.ipynb' -delete
	find notebooks -name '*_removed.ipynb' -delete

dev:
	docker-compose scale dev=1 web=2 ansible=1
	docker-compose logs dev

