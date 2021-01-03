#!/usr/bin/make

SHELL = /bin/sh

UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

run:
	python python-mqtt-client/client.py
build:
	docker build -t client-node:0.1 .
up: 
	docker-compose up -d
shell:
	docker-compose exec client zsh