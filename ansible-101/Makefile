clean:
	rm *.pyc __pycache__ -fr

dev:
	docker-compose scale dev=1 web=2 ansible=1
	docker-compose logs dev

