### Hexlet tests and linter status:

[![Actions Status](https://github.com/poweredbyskx/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/poweredbyskx/python-project-52/actions)
[![Maintainability](https://qlty.sh/badges/59faff8e-9312-470d-a869-8fa742ed3539/maintainability.svg)](https://qlty.sh/gh/poweredbyskx/projects/python-project-52)

Requirements
Python >=3.10
django >= 5.0.2
django-bootstrap5 >= 23.4
postgreSQL >= 16
gunicorn >= 21.2.0
To get started
Clone git repo: git@https://github.com/poweredbysx/python-project-52.git
Go to directory python-project-52: cd python-project-52
Configuring poetry to create a virtual environment: poetry config virtualenvs.in-project true
Create virtual environment and Install dependencies make install
Create .env file in the root folder similar to .env.example
Start app make migrate make static make start