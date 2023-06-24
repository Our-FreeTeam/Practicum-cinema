import json
import logging

import requests
from settings import settings


def create_superuser_requests(new_admin_username: str, new_admin_password: str, target_realm: str):
    # Keycloak Url and master password
    keycloak_url = settings.keycloak_url

    # Obtain access token for the master realm
    token_url = f"{keycloak_url}/realms/master/protocol/openid-connect/token"
    token_data = {
        "username": settings.keycloak_admin_login,
        "password": settings.keycloak_admin_password,
        "grant_type": "password",
        "client_id": "admin-cli",
    }
    token_response = requests.post(token_url, data=token_data)
    access_token = token_response.json()["access_token"]

    # Create new admin user in the target realm
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    new_user_data = {
        "username": new_admin_username,
        "enabled": True,
        "emailVerified": True,
        "attributes": {"timezone": "GMT+0"},
        "email": settings.keycloak_service_email,
        "credentials": [{"type": "password", "value": new_admin_password, "temporary": False}],
    }
    new_user_url = f"{keycloak_url}/admin/realms/{target_realm}/users"
    requests.post(new_user_url, headers=headers, data=json.dumps(new_user_data))

    # Get the new user ID
    user_query_url = f"{keycloak_url}/admin/realms/{target_realm}/" \
                     f"users?username={new_admin_username}"
    user_query_response = requests.get(user_query_url, headers=headers)
    new_user_id = user_query_response.json()[0]["id"]

    # Get the realm-management client ID
    clients_query_url = f"{keycloak_url}/admin/realms/{target_realm}" \
                        f"/clients?clientId={settings.client_id}"
    clients_query_response = requests.get(clients_query_url, headers=headers)
    client_id = clients_query_response.json()[0]["id"]

    # Get the manage-users and manage-roles role IDs
    roles_query_url = f"{keycloak_url}/admin/realms/{target_realm}/clients/{client_id}" \
                      f"/roles?role=theatre_admin"
    roles_query_response = requests.get(roles_query_url, headers=headers)
    client_roles = roles_query_response.json()

    # Assign the manage-users and manage-roles roles to the new admin user
    role_mappings_url = f"{keycloak_url}/admin/realms/{target_realm}/users/{new_user_id}" \
                        f"/role-mappings/clients/{client_id}"
    requests.post(role_mappings_url, headers=headers, data=json.dumps(client_roles))

    logging.info("[SU user created]")
    return True


logging.basicConfig(format=settings.log_format, level=settings.log_level)
create_superuser_requests(settings.keycloak_realm_su, settings.keycloak_realm_su_psw,
                          settings.realm_name)
