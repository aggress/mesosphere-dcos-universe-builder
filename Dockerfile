FROM alpine:latest

MAINTAINER Richard Shaw <rshaw@mesosphere.com>

RUN apk -U add alpine-sdk python3 bash docker py-pip

RUN pip install flask

RUN mkdir /universe-builder

COPY ./bin /universe-buikder

COPY ./web /universe-builder

CMD ["/universe-builder/bin/run.sh main"]
