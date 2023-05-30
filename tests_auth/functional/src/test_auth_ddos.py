import os
import time

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {'Content-Type': "application/json", 'Accept': "application/json", "access_token": "",
           "refresh_token": ""}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body, retry_count, pause',
    [(429, 'POST', 'v1/auth/login', {"user": "", "password": ""}, 500, 0),
     (429, 'POST', 'v1/auth/user_create', {"user": "test_ddos", "password": "test_ddos",
                                           "email": "email@mail.com"},
      500, 0),
     ],

    ids=["DDOS login api", "DDOS Reg form api"]
)
async def test_admin_auth(answer_code: str, req_type: str, api_url: str, body: dict,
                          retry_count: int, pause: int):
    site_url = os.environ.get('AUTH_URL')
    url_params = {'url': site_url + api_url, 'json': body, 'headers': headers}

    result = None
    # for retry in range(retry_count):
    i = 0
    while i < retry_count:
        if req_type == 'GET':
            result = requests.get(**url_params)
        elif req_type == 'POST':
            result = requests.post(**url_params)
        i += 1
        time.sleep(pause)

    assert [result.status_code, retry_count] == [answer_code, i]
