# syntax=docker/dockerfile:1
FROM ubuntu:latest

# install necessary packages using apt
RUN apt update
RUN apt install -y g++
RUN apt install -y python2.7 python2-dev libffi-dev
RUN apt install -y curl
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2.7 get-pip.py
RUN apt install -y openjdk-8-jdk-headless openjdk-8-jre-headless

WORKDIR /app
ADD . /app
# ADD . /sentspace/

RUN pip install JPype-0.5.4.2/
RUN pip install -r ./requirements.txt

# cleanup
RUN apt autoremove -y
RUN pip cache purge
RUN apt clean && rm -rf /var/lib/apt/lists/*

# RUN yarn install --production
# ENTRYPOINT gunicorn flaskproj:app