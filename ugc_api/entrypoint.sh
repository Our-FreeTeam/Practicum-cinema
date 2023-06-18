#!/usr/bin/env bash

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
fi

python wait_for_mongo.py

uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8005
