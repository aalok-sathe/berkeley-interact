# syntax=docker/dockerfile:1
FROM openjdk:18-jdk-slim-buster

# install necessary packages using apt
RUN apt update
RUN apt install -y g++
RUN apt install -y python2.7 python2-dev libffi-dev
RUN apt install -y curl # git
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2.7 get-pip.py
# RUN apt install -y openjdk-8-jdk-headless openjdk-8-jre-headless

WORKDIR /build
COPY ./JPype-0.5.4.2/ /build/JPype-0.5.4.2
RUN pip install JPype-0.5.4.2/
COPY ./requirements.txt /build/
RUN pip install -r ./requirements.txt
RUN rm -rf /build

WORKDIR /app
ADD ./*.py /app/
ADD ./*.sh /app/
ADD ./bin/ /app/bin
ADD ./README.md /app/

# RUN git clone --depth 1 --branch 2.6.0 https://github.com/dmtcp/dmtcp
# RUN cd /app/dmtcp
# RUN ./configure && make && make install
# RUN cd /app

# cleanup
RUN apt autoremove -y
RUN pip cache purge
RUN apt clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/local/openjdk-18

ENTRYPOINT gunicorn interactive:app --preload --config gunicorn_config.py  
CMD -t 10000
