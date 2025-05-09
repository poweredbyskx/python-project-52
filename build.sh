<<<<<<< HEAD
[tool.poetry]
name = "hexlet-code"
version = "0.1.0"
description = ""
authors = ["Mike Kolotovich <k2punk@gmail.com>"]
readme = "README.md"
packages = [{include = "task_manager"}]

[tool.poetry.dependencies]
python = "^3.10"
Django = "^4.1.1"
gunicorn = "^21.2.0"
django-bootstrap5 = "^23.4"
django-filter = "^24.2"
rollbar = "^0.16.3"
python-dotenv = "^1.0.1"
psycopg2-binary = "^2.9.9"
dj-database-url = "^2.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
=======
#!/usr/bin/env bash

# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh || echo "⚠️ Не удалось скачать uv — возможно, проблемы с сетью."

# активация виртуального окружения (если нужно)
if [ -f ../venv/bin/activate ]; then
  source ../venv/bin/activate
else
  echo "⚠️ Виртуальное окружение не найдено по пути ../venv — пропускаем активацию."
fi

# установка зависимостей
uv pip install -r requirements.txt

# выполнение миграций и сборка статики
python manage.py migrate
python manage.py collectstatic --noinput

>>>>>>> 2dc49b9 (Initial commit: project structure, build & render-start targets)
