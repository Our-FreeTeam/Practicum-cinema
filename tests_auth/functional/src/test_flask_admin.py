import pytest
import requests
import os

from dotenv import load_dotenv

load_dotenv()

headers = {'Content-Type': "application/json", 'Accept': "application/json", "access_token": "",
           "refresh_token": ""}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body',
    [(401, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "wrong_pass"}),
     (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
     (200, 'POST', 'v1/admin/check_role', {"roles": ["theatre_admin"]}),
     (403, 'POST', 'v1/admin/check_role', {"roles": ["new_created_role"]}),
     (200, 'POST', 'v1/admin/roles/create', {"role_name": "test_role"}),
     (200, 'POST', 'v1/admin/roles/create', {"role_name": "test_role2"}),
     (200, 'GET', 'v1/admin/roles', ""),
     (200, 'POST', 'v1/admin/roles/test_role2/change', {"role_name": "test_role3"}),
     (200, 'POST', 'v1/admin/roles/test_role3/delete', ""),
     (202, 'POST', 'v1/auth/logout', {"user": "cinema_admin"}),
     (401, 'POST', 'v1/admin/check_role', {"roles": ["theatre_admin"]}),
     (401, 'POST', 'v1/admin/check_role', {"roles": ["new_created_role"]}),
     (401, 'POST', 'v1/admin/roles/create', {"role_name": "test_role"}),
     (401, 'GET', 'v1/admin/roles', ""),
     (401, 'GET', 'v1/admin/user/932cfcaa-1e82-40e3-96a1-74f0e55e9362/roles',
      {"user": "cinema_admin"}),
     (401, 'POST', 'v1/admin/roles/test_role2/delete', ""),
     (401, 'POST', 'v1/admin/roles/test_role2/change', {"role_name": "test_role4"}),
     (401, 'POST', 'v1/admin/grant_role', {"user_name": "test_user", "role_name": "test_role"}),
     (401, 'POST', 'v1/admin/revoke_role', {"user_name": "wrong_user", "role_name": "test_role"}),
     (401, 'POST', 'v1/admin/roles/test_role/delete', {})
     ],

    ids=["Can't login with incorrect admin password",
         "Login with correct admin data",
         "Check yes, i should command all",
         "Can't find not created role yet",
         "Create new test_role",
         "Create new test_role2",
         "Get roles list",
         "Change role for specified user",
         "Delete selected role from system",
         "Logout from system",
         "Check, i should NOT command all",
         "Can't find not created role yet without priv",
         "Can't create new test_role",
         "Can't get roles list",
         "Can't get specified user roles list",
         "Can't delete role for specified user",
         "Can't change role for specified user",
         "Can't add role for specified user",
         "Can't revoke role from specified user",
         "Can't delete selected role from system"
         ]
)
async def test_admin_auth(answer_code: str, req_type: str, api_url: str, body: dict,
                          remove_test_roles):
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code, req_type, api_url, body',
    [
        (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
        (200, 'POST', 'v1/admin/grant_role', {"user_name": "test_user", "role_name": "test_role"}),
        (200, 'GET', 'v1/admin/user/<test_user>/roles', {}),
        (200, 'POST', 'v1/admin/revoke_role', {"user_name": "test_user", "role_name": "test_role"})
    ],
    ids=["Login with correct admin data",
         "Grant role for specified user",
         "Get specified user roles list",
         "Revoke role from specified user"]
)
async def test_admin_user_role(answer_code: str, req_type: str, api_url: str, body: dict,
                               create_remove_test_user_and_role, get_user_id):
    global headers

    site_url = os.environ.get('AUTH_URL')

    user_name = api_url.split('/')
    if len(user_name) > 2:
        user_name = user_name[2]
        if '<' in user_name:
            new_user_name = user_name[1:-1]
            user_id = get_user_id(new_user_name)
            api_url = api_url.replace(user_name, user_id)
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
