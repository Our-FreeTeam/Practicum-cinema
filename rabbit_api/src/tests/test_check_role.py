import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    "access_token": "",
    "refresh_token": ""
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body',
    [
        (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
    ],

    ids=[
        "Login with correct admin data",
    ]
)
async def test_manager_auth(
        answer_code: str, req_type: str, api_url: str, body: dict
):
    global headers

    site_url = os.environ.get('AUTH_URL')
    url_params = {'url': site_url + api_url, 'json': body, 'headers': headers}
    result = None
    if req_type == 'GET':
        result = requests.get(**url_params)
    elif req_type == 'POST':
        result = requests.post(**url_params)

    if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
        headers['access_token'] = result.headers.get("access_token")
        headers['refresh_token'] = result.headers.get("refresh_token")

    assert result.status_code == answer_code
