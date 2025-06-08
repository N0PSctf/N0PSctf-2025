# Use Debian 12 (bookworm) as the base image
FROM debian:bookworm

# Set environment to non-interactive (for clean installs)
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-traditional \
    socat\
    && apt-get clean 

COPY OntheDocker/. .


RUN chmod +x ladybug_app

EXPOSE 1337

# Run ladybug_app when the container starts
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:./ladybug_app"]
