#!/usr/bin/env bash

# this is a wrapper to load aggregate local env variables into a single .env file for docker compose
# then do docker-compose up

# awk .env files into one for docker compose
# https://stackoverflow.com/questions/8183191/concatenating-files-and-insert-new-line-in-between-files
awk '{print $0}' *.env > .env

# start airflow environment
docker compose up -d