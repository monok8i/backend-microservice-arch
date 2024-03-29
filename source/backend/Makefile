current_time := $(shell date '+%Y-%m-%d %H:%M:%S')

.PHONY: app
app:
	docker compose -f ./docker-compose.yaml up -d

.PHONY: drop-all
drop-all:
	docker compose -f ./docker-compose.yaml down
