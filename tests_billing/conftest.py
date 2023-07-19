import pytest
import requests

from tests_billing.functional.utils.helpers import (
    get_auth_headers,
    TEST_USERS_LIST,
    remove_user,
    get_client_id,
    remove_all_test_roles,
    create_test_user,
    TEST_ROLES_LIST,
    create_test_role
)
from tests_billing.settings import settings


keycloak_url = settings.keycloak_url
keycloak_realm_id = settings.keycloak_realm_id


@pytest.fixture(scope='session')
def remove_test_users():
    yield None

    base_url = keycloak_url
    headers = get_auth_headers()
    realm_id = keycloak_realm_id

    for user in TEST_USERS_LIST:
        remove_user(user, base_url, headers, realm_id)


@pytest.fixture(scope='session')
def remove_test_roles():
    yield None
    base_url = keycloak_url
    headers = get_auth_headers()
    client_id = get_client_id(base_url, headers)
    realm_id = keycloak_realm_id

    remove_all_test_roles(base_url, headers, client_id, realm_id)


@pytest.fixture(scope='session')
def create_remove_test_user_and_role():
    base_url = keycloak_url

    headers = get_auth_headers()
    client_id = get_client_id(base_url, headers)
    realm_id = keycloak_realm_id

    for user in TEST_USERS_LIST:
        create_test_user(user, base_url, headers, realm_id)

    for role in TEST_ROLES_LIST:
        create_test_role(role, base_url, headers, client_id)

    yield None

    remove_all_test_roles(base_url, headers, client_id, realm_id)
    for user in TEST_USERS_LIST:
        remove_user(user, base_url, headers, realm_id)


@pytest.fixture(scope='session')
def get_user():
    def inner(username):
        base_url = keycloak_url

        headers = get_auth_headers()
        realm_id = keycloak_realm_id

        user_query_url = f"{base_url}/admin/realms/{realm_id}/users?username={username}"
        user_query_response = requests.get(user_query_url, headers=headers)
        user_id = user_query_response.json()[0]["id"]
        return user_id

    return inner

