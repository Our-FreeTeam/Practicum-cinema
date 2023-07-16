# This is special temporary script to route payments logs from external log service (in internet) to
# local docker components

import requests
from settings import settings
import logging


def main():
    response = requests.get('https://yptst2023.omnitoring.ru:8443/get_logs')
    response.raise_for_status()  # Raise exception if invalid response

    data = response.json()
    if response.status_code == 200:
        logs = data['logs']
        try:
            last_entry = sorted(logs, key=lambda x: x['id'])[-1]
        except Exception:
            logging.info("Error - webhook is empty")
            exit()

        pay_data = last_entry['pay_data']

        post_response = requests.post(
            settings.billing_service_url + '/api/v1/subscriptions/add_2_step',
            json=pay_data)
        if post_response.status_code == 200:
            logging.info("Job done")
        post_response.raise_for_status()  # Raise exception if invalid response
    else:
        logging.error("There is error with request to webhook_log_service {0}".format(response.status_code))


if __name__ == "__main__":
    logging.basicConfig(format=settings.log_format, level=settings.log_level)
    logging.info("Router started")
    main()
