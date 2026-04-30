install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

setup:
	make install && make migrate

build:
	./build.sh

start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:8000

render-start:
	uv run gunicorn task_manager.wsgi

dev:
	uv run python manage.py runserver

lint:
	uv run ruff check .
