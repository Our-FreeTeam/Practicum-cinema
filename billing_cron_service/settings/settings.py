from typing import Optional

from pydantic import BaseSettings, Field


class PGDB(BaseSettings):
    dbname: str = Field(..., env="BILL_DB_NAME")
    user: str = Field(..., env="BILL_DB_USERNAME")
    password: str = Field(..., env="BILL_DB_PASSWORD")
    host: Optional[str] = Field(..., env="BILL_DB_HOST")
    port: int = Field(..., env="BILL_DB_PORT")


class Settings(BaseSettings):
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    realm_name: str = Field(..., env='KEYCLOAK_REALM_ID')
    client_secret_key: str = Field(..., env='KEYCLOAK_SECRET_KEY')
    service_account: str = Field(..., env='KEYCLOAK_SERVICE_ACCOUNT')

    keycloak_admin_login: str = Field(..., env='KEYCLOAK_ADMIN')
    keycloak_admin_password: str = Field(..., env='KEYCLOAK_ADMIN_PASSWORD')
    keycloak_service_email: str = Field(..., env='KEYCLOAK_SERVICE_EMAIL')
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    keycloak_realm_su: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    keycloak_realm_su_psw: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU_PSW')

    debug_mode: int = Field(0, env='BILLING_DEBUG')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
pgdb = PGDB()
