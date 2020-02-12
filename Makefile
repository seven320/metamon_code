
compose/build:
	docker-compose build

compose/up:
	docker-compose up

restart:
	compose/build compose/up

exec:
	docker exec -it hometamon-container /bin/bash
  
run:
	python3 hometamon.py
