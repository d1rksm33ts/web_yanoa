COMPOSE ?= docker compose
PROJECT ?= web-yanoa

.PHONY: config build validate test up down logs

config:
	$(COMPOSE) -p $(PROJECT) config --quiet

build:
	$(COMPOSE) -p $(PROJECT) build

validate:
	./scripts/validate.sh

test: validate
	./scripts/smoke-test.sh

up:
	$(COMPOSE) -p $(PROJECT) up -d --build

down:
	$(COMPOSE) -p $(PROJECT) down

logs:
	$(COMPOSE) -p $(PROJECT) logs -f --tail=100
