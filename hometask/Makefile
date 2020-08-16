export GO111MODULE := off # ???

DBNAME:=hometask
PASSWORD = root
DATASOURCE:=root:$(PASSWORD)@tcp(127.0.0.1:3306)/$(DBNAME)

GOOSE:=$(shell which goose)

# PASSWORD:=root

up:
	docker-compose up -d

down:
	docker-compose down

exec:
	docker exec -it mysql_host bash

migrate/init:
	mysql -u root -p -h 127.0.0.1 --port=3306 --protocol=tcp -e "create database $(DBNAME);"

migrate/up:
	@goose -dir database/migrations mysql "$(DATASOURCE)" up

migrate/down:
	@goose -dir database/migrations mysql "$(DATASOURCE)" down

migrate/new: # make new migrations
	$(GOOSE) -dir database/migrations create $(NAME) sql