#!make

lint:
	ruff check .; ruff check . --diff

format:
	ruff format .; ruff check . --fix

run:
	poetry run fastapi dev dotum/main.py

test:
	poetry run pytest -s -x --cov=dotum -vv; poetry run coverage html