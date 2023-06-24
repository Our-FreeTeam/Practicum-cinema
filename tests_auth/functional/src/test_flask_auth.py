import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {'Content-Type': "application/json", 'Accept': "application/json", "access_token": "",
           "refresh_token": ""}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body',
    [(422, 'POST', 'v1/auth/user_create', {"user": "test_user", "password": "1234567",
                                           "email": "test@mail"}),
     (422, 'POST', 'v1/auth/user_create', {"user": "test_user", "password": "",
                                           "email": "test@mail.com"}),
     (201, 'POST', 'v1/auth/user_create', {"user": "test_user", "password": "123qwer",
                                           "timezone": "GMT+3",
                                           "email": "test@mail.com"}),
     (401, 'POST', 'v1/auth/login', {"user": "test_user", "password": "wrong_pass"}),
     (401, 'POST', 'v1/auth/login', {"user": "wrong_user", "password": "wrong_pass"}),
     (200, 'POST', 'v1/auth/login', {"user": "test_user", "password": "123qwer"}),
     (200, 'POST', 'v1/auth/session_history', {}),
     (202, 'POST', 'v1/auth/user_update', {"user": "test_user", "password": "1234qwer",
                                           "timezone": "GMT+3",
                                           "email": "test@mail.org"}),
     (200, 'POST', 'v1/auth/user_sessions', {}),
     (200, 'POST', 'v1/auth/refresh_token', {}),
     (202, 'POST', 'v1/auth/logout', {"user": "test_user"}),

     (401, 'POST', 'v1/auth/session_history', {}),

     (200, 'POST', 'v1/auth/login', {"user": "test_user", "password": "1234qwer"}),
     (202, 'POST', 'v1/auth/logout', {"user": "test_user"}),

     (401, 'POST', 'v1/auth/user_update', {"user": "test_user", "password": "12123qwer",
                                           "email": "test1@mail1.com"}),
     (401, 'POST', 'v1/auth/user_sessions', {})
     ],
    ids=["Can't reg user with incorrect email",
         "Can't reg user with short password",
         "Create user with right user, pass, email",
         "Can't login with incorrect password",
         "Can't login with wrong username",
         "Login with correct data",
         "Session history",
         "Update user pass and email",
         "Get user sessions list",
         "Refresh user access token",
         'Logout user from system',
         "Can't take session history",
         "Login with new correct data",
         'Logout user from system after second logon',
         "Can't update pass and email after logout",
         "Can't get user sessions list"
         ]
)
async def test_user_auth(answer_code: str, req_type: str, api_url: str, body: dict,
                         remove_test_users):
    global headers

    site_url = os.environ.get('AUTH_URL')
    result = requests.post(url=site_url + api_url, json=body, headers=headers)

    if result.headers.get("access_token") is not None and result.headers.get(
            "refresh_token") is not None:
        headers['access_token'] = result.headers.get("access_token")
        headers['refresh_token'] = result.headers.get("refresh_token")

    assert result.status_code == answer_code
