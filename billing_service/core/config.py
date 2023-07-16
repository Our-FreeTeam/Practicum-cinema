import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field, PostgresDsn, validator

logging_config.dictConfig(LOGGING)


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgresql+asyncpg'}


class Settings(BaseSettings):
    DB_NAME: str = Field("postgres", env="BILL_DB_NAME")
    DB_USER: str = Field("user", env="BILL_DB_USERNAME")
    DB_PASSWORD: str = Field("password", env="BILL_DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="BILL_DB_HOST")
    DB_PORT: str = Field('5438', env="BILL_DB_PORT")

    KASSA_ACCOUNT_ID: str = Field(..., env='KASSA_ACCOUNT_ID')
    KASSA_SECRET_KEY: str = Field(..., env='KASSA_SECRET_KEY')

    DB_URI: AsyncPostgresDsn | None

    CONFIRMATION_URL: str = Field(..., env='CONFIRMATION_URL')
    SUBSCRIPTION_URL: str = Field("localhost", env='SUBSCRIPTION_URL')

    @validator('DB_URI')
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
