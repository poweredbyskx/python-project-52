PORT ?= 8000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv pip install .[dev]

lint:
	flake8 task_manager

static:
	python manage.py collectstatic --noinput

migrate:
	python manage.py makemigrations
	python manage.py migrate

dev: migrate
	python manage.py runserver

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

test:
	python manage.py test

test-coverage:
	coverage run manage.py test
	coverage report -m
	coverage xml

.PHONY: install lint static migrate dev start test
