FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install ncat python3 python3-pip -y

COPY ./src/main.py .
COPY ./requirements.txt ./requirements.txt
COPY ./src/flowers.txt ./flowers.txt
RUN pip install -r requirements.txt --break-system-packages

EXPOSE 1234

RUN useradd -ms /bin/bash challenge
USER challenge

CMD ncat -l -p 1234 --sh-exec "python3 /app/main.py" --keep-open