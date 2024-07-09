date = $(shell date)

.PHONY: migration
migration:
	poetry run alembic -c ./app/database/migrations/alembic.ini revision --autogenerate -m "Revision ($(date))"


.PHONY: migrate
migrate:
	poetry run alembic -c ./app/database/migrations/alembic.ini upgrade head