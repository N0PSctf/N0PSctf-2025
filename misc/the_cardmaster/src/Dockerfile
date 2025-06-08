FROM python:3.12

RUN apt update
RUN apt install wkhtmltopdf poppler-utils -y

WORKDIR /app

COPY requirements.txt ./

COPY .env ./

COPY template.html ./

COPY devlog.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

COPY create_card.sh ./

COPY ./assets/ ./assets/

RUN chmod +x /app/create_card.sh

RUN apt-get remove -y --auto-remove curl
RUN apt-get remove -y --auto-remove wget

RUN useradd -ms /bin/nologin challenge
USER challenge

CMD [ "python", "./main.py" ]
