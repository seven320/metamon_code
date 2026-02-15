# 開発環境起動
dev:
	docker compose build --no-cache
	docker compose up -d

# 本番用
compose/build:
	docker compose build --no-cache

compose/up:
	docker compose up

re-run:
	docker compose down
	docker compose build --no-cache
	docker compose up -d

exec:
	docker exec -it hometamon /bin/sh

test:
	docker compose down
	docker compose build 
	docker compose up -d
	docker exec hometamon pytest tests
	docker compose down
