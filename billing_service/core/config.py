from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field, PostgresDsn, validator

logging_config.dictConfig(LOGGING)


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgresql+asyncpg'}


class Settings(BaseSettings):
    db_name: str = Field("postgres", env="BILL_DB_NAME")
    db_user: str = Field("user", env="BILL_DB_USERNAME")
    db_password: str = Field("password", env="BILL_DB_PASSWORD")
    db_host: str = Field("localhost", env="BILL_DB_HOST")
    db_port: str = Field('5438', env="BILL_DB_PORT")

    kassa_account_id: str = Field(..., env='KASSA_ACCOUNT_ID')
    kassa_secret_key: str = Field(..., env='KASSA_SECRET_KEY')

    db_uri: AsyncPostgresDsn | None

    confirmation_url: str = Field(..., env='CONFIRMATION_URL')
    subscription_url: str = Field("localhost", env='SUBSCRIPTION_URL')

    auth_url: str = Field(..., env='AUTH_URL')
    auth_user: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    auth_password: str = Field(..., env='KK_CINEMAREALM_SU_PSW')
    AUTH_PASSWORD: str = Field(..., env='KK_CINEMAREALM_SU_PSW')

    @validator('db_uri')
    def construct_db_uri(cls, v: str | None, values: dict):
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('db_user'),
            password=values.get('db_password'),
            host=values.get('db_host'),
            path=f'/{values.get("db_name")}',
            port=values.get('db_port'),
        )


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
