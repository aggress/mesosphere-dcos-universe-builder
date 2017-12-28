#!/usr/bin/env bash

docker build -t universe-builder .
docker rm -f /builder
docker run --name=builder -p 127.0.0.1:5000:5000 -v /var/run/docker.sock:/var/run/docker.sock universe-builder:latest
