#!/usr/bin/env bash

python wait_for_keycloak.py
python wait_for_redis.py

export PGPASSWORD=$KC_DB_PASSWORD
psql -h keycloak-postgres -U $KC_DB_USERNAME -f /opt/flaskapi/create_partitioned_tables.sql

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
    echo ========= CREATING SU ===========
    python create_su.py
fi


KC_STATUS_OK="KC_OK.STATUS"
if [ -e /$KC_STATUS_OK ]; then
  gunicorn wsgi:app --bind 0.0.0.0:8001

else
  echo "================== !!! ===================="
  echo "WARNING THERE IS ERRORS WITH KEYCLOAK"
fi


