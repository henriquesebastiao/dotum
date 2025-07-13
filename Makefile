#!make

lint:
	ruff check .; ruff check . --diff

format:
	ruff format .; ruff check . --fix