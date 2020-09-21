FROM python:3.6.12-buster
MAINTAINER Lebedev Aleksandr

WORKDIR /usr/src/pythonserver
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD python main.py

EXPOSE 3000