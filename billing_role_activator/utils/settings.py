from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgresql+asyncpg'}


class Settings(BaseSettings):
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    debug_mode: int = Field(0, env='BILLING_DEBUG')

    db_name: str = Field("postgres", env="BILL_DB_NAME")
    db_user: str = Field("user", env="BILL_DB_USERNAME")
    db_password: str = Field("password", env="BILL_DB_PASSWORD")
    db_host: str = Field("localhost", env="BILL_DB_HOST")
    db_port: str = Field('5438', env="BILL_DB_PORT")
    db_uri: AsyncPostgresDsn | None

    kafka_interface_url: str = Field(..., env='KAFKA_INTERFACE_URL')
    kafka_broker_url: str = Field(..., env='KAFKA_BROKER_URL')

    whok_topic_name: str = Field(..., env='WHOOK_TOPIC_LOG')
    success_pay_topic: str = Field(..., env='SUCCESS_PAY_LOG')
    error_pay_topic: str = Field(..., env='ERROR_PAY_LOG')

    auth_url: str = Field(..., env='AUTH_URL')
    auth_user: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    auth_password: str = Field(..., env='KK_CINEMAREALM_SU_PSW')

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
