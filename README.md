### Hexlet tests and linter status:

[![Actions Status](https://github.com/poweredbyskx/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/poweredbyskx/python-project-52/actions)
[![Maintainability](https://qlty.sh/badges/59faff8e-9312-470d-a869-8fa742ed3539/maintainability.svg)](https://qlty.sh/gh/poweredbyskx/projects/python-project-52)

### Requirements
1. Python >=3.10
2. django >= 5.0.2
3. django-bootstrap5 >= 23.4
4. postgreSQL >= 16
5. gunicorn >= 21.2.0


### To get started
1. Clone git repo:
  `git@https://github.com/poweredbyskx/python-project-52.git`
2. Go to directory python-project-52:
  `cd python-project-52`
3.  Configuring `poetry` to create a virtual environment:
  `poetry config virtualenvs.in-project true`
4.  Create virtual environment and Install dependencies
  `make install`
5. Create `.env` file in the root folder similar to `.env.example`
5. Start app
  `make migrate`
  `make static`
  `make start`