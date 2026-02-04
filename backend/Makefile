.PHONY: install run dev test lint clean migrate migration migrate-down

install:
	poetry install

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest

lint:
	poetry run ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

migrate:
	poetry run alembic upgrade head

generate:
	@read -p "Migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

migrate-down:
	poetry run alembic downgrade -1
