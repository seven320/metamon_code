
compose/build:
	docker-compose build --no-cache

compose/up:
	docker-compose up

re-run:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up

exec:
	docker exec -it hometamon-container /bin/sh
  
run:
	python3 hometamon.py
