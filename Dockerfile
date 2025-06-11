# Container image that runs your code
FROM ubuntu:latest
# Add pandoc
RUN apt-get update && apt-get install -y pandoc
# Add UV to the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY ext/ /ext/
# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
