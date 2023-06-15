#!/usr/bin/env bash

python3 /tests_analytic/functional/wait_for_fastapi.py


CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
FA_STATUS_OK="FA_OK.STATUS"


if [ -e /$FA_STATUS_OK ]; then
  pytest /tests_analytic/functional/src --hs_access_token="$HELIOS_API_TOKEN" --hs_enabled=false
else
  echo "================== !!! ===================="
  echo "WARNING THERE IS ERRORS WITH FASTAPI check"
fi