#!/bin/bash
# singularity exec docker://aloxatel/berkeleyparser /bin/bash -c "JAVA_HOME=/usr/local/openjdk-18 gunicorn interactive:app --config gunicorn_config.py" 
# singularity exec docker://aloxatel/berkeleyparser /bin/bash -c "JAVA_HOME=/usr/local/openjdk-18 gunicorn interactive:app -t 15 --preload --config gunicorn_config.py" 
singularity exec docker://aloxatel/berkeleyparser /bin/bash -c "JAVA_HOME=/usr/local/openjdk-18 gunicorn interactive:app --preload --config gunicorn_config.py " 
# singularity run --no-home docker://aloxatel/berkeleyparser:latest
