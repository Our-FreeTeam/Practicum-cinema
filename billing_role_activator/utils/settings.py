from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgresql+asyncpg'}


class Settings(BaseSettings):
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    debug_mode: int = Field(0, env='BILLING_DEBUG')

    DB_NAME: str = Field("postgres", env="BILL_DB_NAME")
    DB_USER: str = Field("user", env="BILL_DB_USERNAME")
    DB_PASSWORD: str = Field("password", env="BILL_DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="BILL_DB_HOST")
    DB_PORT: str = Field('5438', env="BILL_DB_PORT")
    DB_URI: AsyncPostgresDsn | None

    kafka_interface_url: str = Field(..., env='KAFKA_INTERFACE_URL')
    kafka_broker_url: str = Field(..., env='KAFKA_BROKER_URL')

    whok_topic_name: str = Field(..., env='WHOOK_TOPIC_LOG')
    success_pay_topic: str = Field(..., env='SUCCESS_PAY_LOG')
    error_pay_topic: str = Field(..., env='ERROR_PAY_LOG')

    AUTH_URL: str = Field(..., env='AUTH_URL')
    AUTH_USER: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    AUTH_PASSWORD: str = Field(..., env='KK_CINEMAREALM_SU_PSW')

    @validator('DB_URI', pre=True)
    def construct_db_uri(cls, v: str | None, values: dict):
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            path=f'/{values.get("DB_NAME")}',
            port=values.get('DB_PORT'),
        )

class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
