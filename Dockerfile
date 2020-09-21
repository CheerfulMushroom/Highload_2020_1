FROM python:3.6.12-buster
MAINTAINER Lebedev Aleksandr

WORKDIR /usr/src/pythonserver
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8888