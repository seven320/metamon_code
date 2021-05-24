
compose/build:
	docker-compose build --no-cache

compose/up:
	docker-compose up

re-run:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

exec:
	docker exec -it hometamon /bin/sh
  
test:
	docker-compose down
	docker-compose build 
	docker-compose up -d
	docker exec hometamon pytest tests

# run:
	# python3 main/src/hometamon.py --test 1
