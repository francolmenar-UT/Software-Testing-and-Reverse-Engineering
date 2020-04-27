#!/usr/bin/env bash
# Cleans and set up the docker
docker stop $(docker ps -a -q)

docker rm $(docker ps -a -q)

docker run -it str_container /bin/bash
