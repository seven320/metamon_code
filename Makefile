compose/build:
	docker-compose build

compose/up:
	docker-compose up

restart:
	compose/build compose/up
