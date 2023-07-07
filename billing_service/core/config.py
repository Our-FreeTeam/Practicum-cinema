import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    db_name: str = Field("postgres", env="BILL_DB_NAME")
    db_user: str = Field("postgres", env="BILL_DB_USERNAME")
    db_password: str = Field("password", env="BILL_DB_PASSWORD")
    db_host: str = Field("localhost", env="BILL_DB_HOST")
    db_port: str = Field('5432', env="BILL_DB_PORT")

    kassa_account_id: str = Field(..., env='KASSA_ACCOUNT_ID')
    kassa_secret_key: str = Field(..., env='KASSA_SECRET_KEY')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
