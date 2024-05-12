date = $(shell date)

.PHONY: migration
migration:
	alembic revision --autogenerate -m "Revision ($(date))"


.PHONY: migrate
migrate:
	alembic upgrade head