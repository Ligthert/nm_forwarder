FROM ubuntu:16.04

ADD nm_forwarder /nm_forwarder
ADD requirements.txt /requirements.txt

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

WORKDIR /
ENTRYPOINT /nm_forwarder
