FROM python:latest

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY ./src .
COPY ./flag.txt .passwd

RUN useradd -ms /bin/bash challenge
USER challenge

CMD [ "python3", "./app.py"]