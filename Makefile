.PHONY: up-prod down-prod build-prod run-prod

build-prod:
	docker-compose -f docker-compose.yml build --no-cache

up-prod:
	docker-compose -f docker-compose.yml up -d

down-prod:
	docker-compose -f docker-compose.yml down -v

run-prod:
	docker-compose -f docker-compose.yml up -d --build
	docker-compose -f docker-compose.yml exec -T netology-prototype-stage-api sh -c "sleep 10 && alembic upgrade head"