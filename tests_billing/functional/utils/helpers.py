import json
from contextlib import contextmanager

import psycopg2
import requests
from psycopg2.extras import DictCursor

from tests_billing.settings import pgdb, settings
from tests_billing.functional.utils.backoff import log, backoff

TEST_USERS_LIST = ["test_user"]
TEST_ROLES_LIST = ["test_role"]
HEADERS = {'Content-Type': "application/json", 'Accept': "application/json", "access_token": "",
           "refresh_token": ""}
keycloak_realm_id = settings.keycloak_realm_id
keycloak_client_id = settings.keycloak_client_id
duration = {
    "59507685-5b50-4d60-b4d1-6fc0ab1bacd1": 12,
    "339052fe-9f44-4c03-8ccf-e11b9629d6d1": 1,
    }


@log
@backoff(exception=psycopg2.OperationalError)
def pg_conn(*args, **kwargs):
    return psycopg2.connect(*args, **kwargs)


@contextmanager
def pg_conn_context(*args, **kwargs):
    connection = pg_conn(*args, **kwargs)
    yield connection
    connection.close()


def get_auth_headers():
    token_url = f"{settings.keycloak_url}/realms/master/protocol/openid-connect/token"

    token_data = {
        "username": settings.keycloak_admin_login,
        "password": settings.keycloak_admin_psw,
        "grant_type": "password",
        "client_id": "admin-cli",
    }
    token_response = requests.post(token_url, data=token_data)
    access_token = token_response.json()["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers


def get_client_id(base_url: str, headers: dict):
    clients_query_url = f"{base_url}/admin/realms/{keycloak_realm_id}" \
                        f"/clients?clientId={keycloak_client_id}"
    clients_query_response = requests.get(clients_query_url, headers=headers)
    client_id = clients_query_response.json()[0]["id"]

    return client_id


def create_test_user(username, base_url, headers, realm_name):
    new_user_data = {
        "username": username,
        "enabled": True,
        "emailVerified": True,
        "credentials": [{"type": "password", "value": username, "temporary": False}],
    }
    new_user_url = f"{base_url}/admin/realms/{realm_name}/users"
    requests.post(new_user_url, headers=headers, data=json.dumps(new_user_data))


def create_test_role(rolename, base_url, headers, client_id):
    new_role_url = f"{base_url}/admin/realms/{keycloak_realm_id}/clients/" \
                   f"{client_id}/roles"
    new_role_data = {
        "name": rolename,
        "description": "",
        "attributes": {}
    }
    requests.post(new_role_url, headers=headers, data=json.dumps(new_role_data))


def remove_all_test_roles(base_url, headers, client_id, realm_id):
    roles_url = f"{base_url}/admin/realms/{realm_id}/clients/" \
                f"{client_id}/roles"
    roles = requests.get(roles_url, headers=headers).json()
    for role in roles:
        if role['name'] in TEST_ROLES_LIST:
            requests.delete(f'{base_url}/admin/realms/cinema/roles-by-id/{role["id"]}',
                            headers=headers)


def remove_user(username, base_url, headers, realm_id):
    users_url = f"{base_url}/admin/realms/{realm_id}/users"

    user_id = requests.get(users_url, params={'username': username}, headers=headers).json()[0][
        'id']
    requests.delete(f'{users_url}/{user_id}', headers=headers)


async def get_active_subscription(user_id):
    sql = f"""
        SELECT * FROM subscription s WHERE s.user_id = '{user_id}' AND s.is_active = True
    """
    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql)
        subscription = cur.fetchone()

    return subscription


def get_payment_id(subscription_id):
    sql = f"""
        SELECT * FROM payment p WHERE p.subscription_id = '{subscription_id}'
    """
    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql)
        payment = cur.fetchone()

    return payment
