FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install poppler-utils