FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install ncat python3 -y

COPY ./src/main.py .
COPY ./flag.txt .passwd

EXPOSE 1234

RUN useradd -ms /bin/bash challenge
USER challenge

CMD ncat -l -p 1234 --sh-exec "python3 /app/main.py" --keep-open