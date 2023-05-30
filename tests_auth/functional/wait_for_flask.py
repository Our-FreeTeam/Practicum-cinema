import logging
import time

import backoff
import requests
from settings import settings


@backoff.on_exception(backoff.expo,
                      requests.exceptions.ConnectionError,
                      max_tries=8,
                      jitter=None)
def connect_check():
    logging.info("[Trying check health status of FlaskAUTH api]")
    result = requests.get(settings.auth_url + "v1/auth/login")
    if result.status_code == 405:
        with open("/FL_OK.STATUS", "w") as fp:
            fp.write("ok")
            logging.info("[FlaskAUTH OK]")


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    time.sleep(4)
    connect_check()
