current_time := $(shell date '+%Y-%m-%d %H:%M:%S')

.PHONY: app
app:
	docker compose -f ./docker-compose.yaml up -d

.PHONY: watch
watch:
	docker compose -f ./docker-compose.yaml watch

.PHONY: stop-all
stop-all:
	docker compose -f ./docker-compose.yaml stop

.PHONY: drop-all
drop-all:
	docker compose -f ./docker-compose.yaml down
