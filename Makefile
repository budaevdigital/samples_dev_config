.PHONY: build up stop down restart logging pip start

PROJECT ?= <ИМЯ ПРОЕКТА>
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)
include ./.env


default: help

help: Makefile
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'

## make start: команда для билда всех контейнеров проекта
start: build up migrations

## make build: команда для создания заданного контейнера проекта
build:
	docker compose -p ${PROJECT} build

## make test: команда для старта тесто
test:
	docker compose -p ${PROJECT} run --rm -e POSTGRES_DB=${PROJECT}_test <НАЗВАНИЕ СЕРВИСА> \
		pytest tests/${FILE} --asyncio-mode=auto -p no:warnings --tb=native -vv --setup-show --cov=src --trace-config -s ${CMD}

## make up: команда для старта заданного проекта (например, PROFILES='--profile main --profile crons')
up:
	docker compose -p ${PROJECT} ${PROFILES} up -d --remove-orphans

## make down: команда для остановки конкретного контейнера
stop:
	docker compose stop ${PROJECT}

## make down: команда для остановки заданного контейнера
down:
	docker compose -p ${PROJECT} -v down --rmi all

## make clear: команда для чистки кэша python
clear:
	find . -name \*.pyc -delete && find . -name "__pycache__" -delete

## make upgrade_migration: команда для создания новой ревизии
upgrade_migration:
	docker compose -p ${PROJECT} run --rm --no-deps ${PROJECT} alembic revision --autogenerate -m "${MESSAGE}"

## make up_migrations: команда для запуска всех миграций бд
migrations:
	docker compose -p ${PROJECT} run --rm ${PROJECT} \
		alembic upgrade head

## make downgrade_last_migration: команда для отката последней ревизии
downgrade_last_migration:
	docker compose -p ${PROJECT} run --rm -e POSTGRES_DBNAME=${PROJECT} ${PROJECT} \
		alembic downgrade -1

## make logging: команда для отображения логов заданного приложения
logging:
	docker compose -p ${PROJECT} logs -f --tail="100" ${PROJECT}

## make ps: команда для вывода списка всех запушенных контейнеров
ps:
	docker compose -p ${PROJECT} ps

## make restart: команда для перезапуска заданного контейнера
restart:
	docker compose -p ${PROJECT} restart ${PROJECT}

## make check: проверка кода с линтером ruff (make check VALUE=--unsafe-fixes)
check:
	ruff check ./src ${VALUE}

## make format: проверка кода с форматтером ruff
format:
	ruff format ./src ${VALUE}
