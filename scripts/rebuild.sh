#!/usr/bin/env bash

docker build -t universe-builder .

docker run -it -v /var/run/docker.sock:/var/run/docker.sock universe-builder:latest /bin/bash