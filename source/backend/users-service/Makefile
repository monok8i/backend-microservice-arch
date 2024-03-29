current_time := $(shell date '+%Y-%m-%d %H:%M:%S')

.PHONY: migration
migration:
	poetry run alembic revision --autogenerate -m "Revision $(current_time)"

.PHONY: migrate
migrate:
	poetry run alembic upgrade head