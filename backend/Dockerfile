FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev

ADD building_hack/backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN rm /requirements.txt
ADD building_hack/backend/app /app

RUN mkdir /files # for files, e.g. xls

WORKDIR /app

