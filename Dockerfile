FROM alpine:latest

MAINTAINER Richard Shaw <richard@aggress.net>

RUN apk -U add alpine-sdk python3 bash docker py-pip

RUN pip install flask

RUN mkdir -p /universe-builder

COPY ./bin /universe-builder/bin

COPY ./web /universe-builder/web

EXPOSE 5000/tcp

WORKDIR /

CMD ["/universe-builder/bin/run.sh", "main"]
