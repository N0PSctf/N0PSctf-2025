FROM python:latest

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY ./src .

CMD [ "python3", "./app.py"]