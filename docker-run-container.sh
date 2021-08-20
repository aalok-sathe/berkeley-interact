#!/bin/bash
sudo docker run -it --net=host --expose 8000 -p 8000:8000 -v ~/code/docker/berkeleyinteract:/app aloxatel/berkeleyparser:latest