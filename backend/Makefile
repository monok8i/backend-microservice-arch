current_time := $(shell date '+%Y-%m-%d %H:%M:%S')
dc = docker compose
dc_yaml = ./docker-compose.yaml

.PHONY: app
app:
	${dc} -f ${dc_yaml} up -d

.PHONY: build
build:
	${dc} -f ${dc_yaml} up --build

.PHONY: stop-all
stop-all:
	${dc} -f ${dc_yaml} stop

.PHONY: drop-all
drop-all:
	${dc} -f ${dc_yaml} down
