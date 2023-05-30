#!/usr/bin/env bash

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
    echo ========= CREATING TOPIC ===========
    python create_topic.py
fi

python wait_for_kafka.py

uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8004
