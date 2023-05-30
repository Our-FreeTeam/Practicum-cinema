from settings import settings

from keycloak import KeycloakAdmin, KeycloakOpenID, KeycloakOpenIDConnection

keycloak_conn = KeycloakOpenID(server_url=settings.keycloak_url,
                               client_id=settings.client_id,
                               realm_name=settings.realm_name,
                               client_secret_key=settings.client_secret_key)

keycloak_admin_conn = KeycloakOpenIDConnection(
    server_url=settings.keycloak_url,
    username=settings.keycloak_realm_su,
    password=settings.keycloak_realm_su_psw,
    realm_name=settings.realm_name,
    user_realm_name=settings.realm_name,
    client_id=settings.client_id,
    client_secret_key=settings.client_secret_key,
    verify=True)

keycloak_admin = KeycloakAdmin(server_url=settings.keycloak_url, connection=keycloak_admin_conn)
