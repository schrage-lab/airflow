#!/usr/bin/env bash

# this is a wrapper to load shared (in the lab) but secret (to the world) environment variables from
# our shared file server and overwrite the local .env variables, then do docker-compose up

# get env variables to get location of airflow variables
# https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs
export $(grep -v '^#' .env | xargs)

# read shared airflow variables
readarray -t keys < "${SHARED_AIRFLOW_KEYS_LOCATION}"

# parse the shared airflow variables into key-value pairs and then replace the .env variables appropriately
# https://stackoverflow.com/questions/11245144/replace-whole-line-containing-a-string-using-sed
for i in "${keys[@]}"; do
  key=$( cut -d '=' -f 1 <<< "$i" );
  value=$( cut -d '=' -f 2- <<< "$i" );
  sed -i "s/.*${key}.*/${key}=${value}/" .env
done

# start airflow environment
docker compose up