.PHONY: up-prod down-prod build-prod run-prod

build-prod:
	sudo docker compose build --no-cache

up-prod:
	sudo docker compose up -d

down-prod:
	sudo docker compose down -v

run-prod:
	sudo docker compose up -d --build