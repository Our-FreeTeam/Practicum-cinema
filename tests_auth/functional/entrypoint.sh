#!/usr/bin/env bash

python3 /tests_auth/functional/wait_for_keycloak.py
python3 /tests_auth/functional/wait_for_flask.py


CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
KC_STATUS_OK="KC_OK.STATUS"
FL_STATUS_OK="FL_OK.STATUS"


if [ -e /$KC_STATUS_OK ] && [ -e /$FL_STATUS_OK ]; then
  pytest /tests_auth/functional/src --hs_access_token="$HELIOS_API_TOKEN" --hs_enabled=true
else
  echo "================== !!! ===================="
  echo "WARNING THERE IS ERRORS WITH KEYCLOAK or FLASKAUTH check"
fi