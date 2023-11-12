FROM python:3.8-slim-buster


WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y poppler-utils
RUN pip3 install -r requirements.txt