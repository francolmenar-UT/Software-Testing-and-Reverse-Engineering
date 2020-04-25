#!/usr/bin/env bash

docker_id=$(docker ps -aqf "ancestor=str_container") # Get docker's id

mkdir "../results/"

# Copying the folders
docker cp "$docker_id":/home/str/astor/output_astor/ ../results/
