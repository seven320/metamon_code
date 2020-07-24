export GO111MODULE := off # ???

DBNAME:=hometask
DATASOURCE:=root:password@tcp(127.0.0.1:3306)/$(DBNAME)

GOOSE:=$(shell which goose)

PASSWORD:=password

up:
	docker-compose up -d

down:
	docker-compose down

exec:
	docker exec -it database_hometask_1 bash

migrate/init:
	mysql -u root -p -h 127.0.0.1 --port=3306 --protocol=tcp -e "create database $(DBNAME);"

migrate/up:
	@goose -dir migrations mysql "$(DATASOURCE)" up

migrate/down:
	@goose -dir migrations mysql "$(DATASOURCE)" down

migrate/new: # make new migrations
	$(GOOSE) -dir migrations create $(NAME) sql