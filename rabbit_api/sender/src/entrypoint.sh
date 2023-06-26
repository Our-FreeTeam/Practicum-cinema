#!/usr/bin/env bash


CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
    echo ========= CREATING Delayed Q ===========
#    python3 /app/utils/create_delayed_exchange.py
fi


python3 sender.py



