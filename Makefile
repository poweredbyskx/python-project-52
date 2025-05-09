<<<<<<< HEAD
dev:
	python3 manage.py runserver
install:
	poetry install
messages:
	python3 ../../manage.py makemessages -l ru
compile:
	python3 ../manage.py compilemessages
build:
	./build.sh
=======
PORT ?= 8000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	poetry install

render-start:
	gunicorn hexlet_code.wsgi

lint:
	poetry run flake8 task_manager

collect-ru:
	poetry run django-admin makemessages -l ru

collect-en:
	poetry run django-admin makemessages -l en

compile-texts:
	poetry run django-admin compilemessages

static:
	poetry run python manage.py collectstatic --noinput

2superuser:
	poetry run python manage.py createsuperuser

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev: migrate
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py

.PHONY: install lint static migrate dev start test
>>>>>>> 2dc49b9 (Initial commit: project structure, build & render-start targets)
