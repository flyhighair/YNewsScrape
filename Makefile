.PHONY: lint format format-check typecheck check run

lint:
		poetry run pflake8 .

format:
		poetry run black .

format-check:
		poetry run black . --check

typecheck:
		poetry run mypy .

check:
		@make lint
		@make format-check
		@make typecheck

run:
		poetry run python -m ynewsscrape
