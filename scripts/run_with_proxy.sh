#!/usr/bin/env bash

docker ps --format '{{.Names}}' | grep registry || docker rm -f /registry > /dev/null 2>&1
docker ps --format '{{.Names}}' | grep builder || docker rm -f /builder > /dev/null 2>&1
docker run --name=builder -e "http_proxy=http://myproxy.example.com:8080" -e "https_proxy=https://myproxy.example.com:8080" -p 127.0.0.1:5001:5001 -v /var/run/docker.sock:/var/run/docker.sock aggress/universe-builder:latest
