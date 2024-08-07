FROM ubuntu:latest

RUN apt-get update && apt-get install python pip
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]