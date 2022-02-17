#!/usr/bin/env bash

# this is a wrapper to load shared (in the lab) but secret (to the world) environment variables from
# our shared file server and overwrite the local .env.redcap variables, then do docker-compose up

# get env variables to get location of airflow variables
# https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs
shopt -s dotglob
export $(grep -v '^#' .fs.env | xargs)

# read shared airflow variables
shared=$(<"${SHARED_AIRFLOW_KEYS_LOCATION}")

# awk .env files into one for docker compose
# https://stackoverflow.com/questions/8183191/concatenating-files-and-insert-new-line-in-between-files
awk '{print $0}' *.env > .env

echo "$shared" >> .env

# start airflow environment
docker compose up -d