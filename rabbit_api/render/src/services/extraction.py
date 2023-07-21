from http import HTTPStatus

import backoff
import psycopg2
import requests


class UserDataExtractor:
    def __init__(self, endpoint: str, authorization: str) -> None:
        self.headers = {
            "Authorization": authorization,
        }
        self.url = endpoint

    @backoff.on_exception(
        backoff.expo,
        exception=psycopg2.OperationalError,
        max_tries=6
    )
    def get_info(self, user_id: str) -> dict:
        response = requests.get(url=f"{ self.url}/{user_id}", headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Status code {response.status_code} {response.text}")
        return response.json()
