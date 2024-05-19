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

.PHONY: stop
stop:
	@if [ -z "$(name)" ]; then \
		echo "Please provide the container name using 'make stop name=<container_name>'"; \
	else \
		if docker ps -q -f name=$(name) | grep -q .; then \
			docker stop -t 1 $(name); \
		else \
			echo "Container $(name) not found or already stopped."; \
		fi \
	fi

.PHONY: drop-all
drop-all:
	${dc} -f ${dc_yaml} down
