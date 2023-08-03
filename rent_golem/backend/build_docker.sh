#!/usr/bin/env bash

docker-compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
