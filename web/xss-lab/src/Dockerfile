FROM python:latest

WORKDIR /app

RUN pip install Flask
RUN pip install selenium

RUN apt update
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb 

COPY ./src/ .

EXPOSE 80

CMD [ "python", "./app.py" ]