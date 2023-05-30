import backoff
import requests
import time

from settings import settings
import logging


@backoff.on_exception(backoff.expo,
                      requests.exceptions.ConnectionError,
                      max_tries=8,
                      jitter=None)
def connect_check():
    logging.info("[Trying check health status of Keycloak]")
    result = requests.get(settings.keycloak_url + "/health")
    if result.content.decode('utf-8').find('"status": "UP"') > 0:
        with open("/KC_OK.STATUS", "w") as fp:
            fp.write("ok")
            logging.info("[KeyCloak OK]")


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    time.sleep(4)
    connect_check()
