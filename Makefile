.PHONY: build up down test lint scan clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

test:
	docker compose up -d
	sleep 5
	curl -f http://localhost:8000/ || exit 1
	curl -f http://localhost:8000/api/info || exit 1
	docker compose exec app id -u | grep -v "^0$$" || exit 1
	docker compose ps | grep "healthy" || exit 1

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

scan:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy image secure-app:latest

clean:
	docker compose down -v
	docker rmi secure-app:latest || true

