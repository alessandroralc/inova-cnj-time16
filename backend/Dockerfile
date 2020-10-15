FROM python:3.7-slim-buster

ENV DEBIAN_FRONTEND="noninteractive"

RUN export DEBIAN_FRONTEND=noninteractive \
    && echo "America/Sao_Paulo" > /etc/timezone \
    && mkdir /home/flask-api \
    && apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install gcc \
    && apt-get -y install libpq-dev \
    && apt-get -y install libaio-dev \
    && mkdir -p /opt/data/api \
    && apt-get clean all 

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /home/flask-api/

COPY ./flask-api .

EXPOSE 5002
