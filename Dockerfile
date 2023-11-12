FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y poppler-utils

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt