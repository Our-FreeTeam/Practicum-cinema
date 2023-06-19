import json
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus

import requests

logger = logging.getLogger()


class URLShortener(ABC):
    @abstractmethod
    def short(self, url: str) -> str:
        """Method shorten url.
        Args:
            url: URL to short.
        Returns:
            str: short url.
        """
        pass


class BitlyURLShortener(URLShortener):
    def __init__(self, endpoint: str, access_token: str,) -> None:
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}"
                        }
        self.endpoint = endpoint

    def short(self, url: str) -> str:
        data = {
            "long_url": url
        }
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                data=json.dumps(data),
                verify=False,
            )
            if response.status_code == HTTPStatus.OK:
                return response.json()["link"]

            logger.error("Bitly error %s %s", response.status_code, response.content)
        except BaseException:
            logger.exception("Error to short url.")
        return url
