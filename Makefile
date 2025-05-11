.PHONY: up-prod down-prod build-prod run-prod

build-prod:
	docker-compose -f docker-compose.yml build --no-cache

up-prod:
	docker-compose -f docker-compose.yml up -d

down-prod:
	docker-compose -f docker-compose.yml down -v

run-prod:
	docker-compose -f docker-compose.yml up -d --build