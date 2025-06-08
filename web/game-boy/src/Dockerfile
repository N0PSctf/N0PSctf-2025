FROM python:latest

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY ./src .

COPY ./mysql /docker-entrypoint-initdb.d
RUN chmod -R 755 /docker-entrypoint-initdb.d

CMD [ "python3", "./app.py"]