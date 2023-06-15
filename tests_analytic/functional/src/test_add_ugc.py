import os

import pytest
import requests
from dotenv import load_dotenv

from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

load_dotenv()

headers = {'Content-Type': "application/json", 'Accept': "application/json", "access_token": "",
           "refresh_token": ""}

site_url = os.environ.get('AUTH_URL')
analytic_url = os.environ.get('ANALYTIC_URL')
keycloak_url = os.environ.get('KEYCLOAK_URL')
keycloak_realm = os.environ.get('KEYCLOAK_REALM_ID')
keycloak_client_id = os.environ.get('KEYCLOAK_CLIENT_ID')
keycloak_client_secret = os.environ.get('KEYCLOAK_SECRET_KEY')

keycloak_admin_name = os.environ.get('KEYCLOAK_ADMIN')
keycloak_admin_psw = os.environ.get('KEYCLOAK_ADMIN_PASSWORD')


def get_user_id(user_name) -> str:
    keycloak_admin_conn = KeycloakOpenIDConnection(
        server_url=keycloak_url,
        username=keycloak_admin_name,
        password=keycloak_admin_psw,
        realm_name=keycloak_realm,
        client_id=keycloak_client_id,
        client_secret_key=keycloak_client_secret,
        verify=True)

    keycloak_admin = KeycloakAdmin(server_url=keycloak_url, connection=keycloak_admin_conn)
    return keycloak_admin.get_user_id(user_name)


user_id = get_user_id("cinema_admin")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body',
    [(401, 'POST', site_url + 'v1/auth/login', {"user": "test_user", "password": "wrong_pass"}),
     (401, 'POST', analytic_url + '/api/v1/events/create',
      {"user": "cinema_admin", "password": "wrong_pass",
       "user_id": user_id,
       "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
       "event_type": 10,
       "message": 1234}),

     (200, 'POST', site_url + 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
     (200, 'POST', analytic_url + '/api/v1/events/create', {"user_id": user_id,
                                                            "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                                                            "event_type": 10,
                                                            "message": 1234}),

     (200, 'GET',
      analytic_url + f'/api/v1/views/get_last_view?user_id={user_id}&movie_id=3fa85f64-5717-4562-b3fc-2c963f66afa2',
      {}),

     (200, 'POST', analytic_url + '/api/v1/events/create', {"user_id": user_id,
                                                            "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                                                            "event_type": 20,
                                                            "message": 1234}),

     (200, 'GET',
      analytic_url + f'/api/v1/views/get_like?user_id={user_id}&movie_id=3fa85f64-5717-4562-b3fc-2c963f66afa2',
      {}),


     (202, 'POST', site_url + 'v1/auth/logout', {"user": "cinema_admin", "password": "password"}),
     (401, 'POST', analytic_url + '/api/v1/events/create', {"user_id": user_id,
                                                            "movie_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                                                            "message": 1234}),
     ],
    ids=["Can't login with incorrect pass",
         "Can't save user event in Kafka without login",
         "Login into service",
         "Save user frame for movie",
         "Get frame in movie for user",
         "Save user like for movie",
         "Get user like for movie",
         "Logout from service",
         "Can't save user event in Kafka"
         ]
)
async def test_user_auth(answer_code: str, req_type: str, api_url: str, body: dict):
    global headers

    if req_type == "POST":
        result = requests.post(url=api_url, json=body, headers=headers)
    else:
        result = requests.get(url=api_url, headers=headers)

    if result.headers.get("access_token") is not None and result.headers.get(
            "refresh_token") is not None:
        headers['access_token'] = result.headers.get("access_token")
        headers['refresh_token'] = result.headers.get("refresh_token")

    assert result.status_code == answer_code
