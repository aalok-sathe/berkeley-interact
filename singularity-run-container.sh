#!/bin/bash
singularity exec docker://aamirov/berkeleyparser /bin/bash -c "JAVA_HOME=/usr/local/openjdk-18 gunicorn interactive:app -t 100 --preload --config gunicorn_config.py"
# singularity run --no-home docker://aloxatel/berkeleyparser:latest
