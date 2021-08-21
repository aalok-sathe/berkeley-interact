#!/bin/bash
singularity exec docker://aloxatel/berkeleyparser /bin/bash -c "JAVA_HOME=/usr/local/openjdk-18 gunicorn interactive:app -t 1000"
# singularity run --no-home docker://aloxatel/berkeleyparser:latest
