#!/usr/bin/env bash

python3 /tests/functional/utils/wait_for_es.py
python3 /tests/functional/utils/wait_for_redis.py


CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
ES_STATUS_OK="ES_OK.STATUS"
RD_STATUS_OK="RD_OK.STATUS"

if [ ! -e /$CONTAINER_FIRST_STARTUP ] && [ -e /$ES_STATUS_OK ] && [ -e /$RD_STATUS_OK ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
    /tests/functional/utils/create_es_schema.sh
fi

if [ -e /$ES_STATUS_OK ] && [ -e /$RD_STATUS_OK ]; then
  pytest /tests/functional/src
else
  echo "================== !!! ===================="
  echo "WARNING THERE IS ERRORS WITH ES or RD check"
fi