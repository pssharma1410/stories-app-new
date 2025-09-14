.PHONY: dev test lint migrate worker

dev:
	docker-compose up --build

migrate:
	docker-compose run --rm web python api/manage.py migrate

superuser:
	docker-compose run --rm web python api/manage.py createsuperuser

worker:
	docker-compose run --rm worker

lint:
	flake8 .

test:
	pytest
