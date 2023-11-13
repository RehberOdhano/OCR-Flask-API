FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install scikit-learn
RUN pip3 install pdf-info
RUN pip3 install -r requirements.txt