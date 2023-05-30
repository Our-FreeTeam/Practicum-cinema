import backoff
import requests
import logging
import time

from settings import settings


@backoff.on_exception(backoff.expo,
                      requests.exceptions.ConnectionError,
                      max_tries=8,
                      jitter=None)
def connect_check():
    logging.info("[Trying check health status of FastAPI analytic api]")
    result = requests.get(settings.analytic_url + "/api/v1/views/get_last_view")
    if result.status_code == 422:
        with open("/FA_OK.STATUS", "w") as fp:
            fp.write("ok")
            logging.info("[FastAPI OK]")


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    time.sleep(4)
    connect_check()
