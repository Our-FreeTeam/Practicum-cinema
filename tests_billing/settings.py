from typing import Optional

from pydantic import BaseSettings, Field


class PGDB(BaseSettings):
    dbname: str = Field(..., env="BILL_DB_NAME")
    user: str = Field(..., env="BILL_DB_USERNAME")
    password: str = Field(..., env="BILL_DB_PASSWORD")
    host: Optional[str] = Field(..., env="BILL_DB_HOST")
    port: int = Field(..., env="BILL_DB_PORT")


class Settings(BaseSettings):
    subscription_url: str = Field(..., env='SUBSCRIPTION_URL')

    keycloak_realm_id: str = Field(..., env='KEYCLOAK_REALM_ID')
    keycloak_client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    keycloak_admin_login: str = Field(..., env='KEYCLOAK_ADMIN_LOGIN')
    keycloak_admin_psw: str = Field(..., env='KEYCLOAK_ADMIN_PSW')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
pgdb = PGDB()
