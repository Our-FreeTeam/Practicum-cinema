import logging
from enum import Enum
from logging import config as logging_config

from dotenv import find_dotenv
from pydantic import BaseSettings, Field

# Применяем настройки логирования
from config.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Postgres(BaseSettings):
    # Настройки Redis
    dbname: str = Field("notifications", env="POSTGRES_DB")
    user: str = Field("postgres", env="POSTGRES_USER")
    password: str = Field("password", env="POSTGRES_PASSWORD")
    host: str = Field("localhost", env="POSTGRES_HOST")
    port: int = Field(5432, env="POSTGRES_PORT")


class RabbitMQ(BaseSettings):
    username: str = Field("guest", env="RABBIT_USER")
    password: str = Field("password", env="RABBIT_PASSWORD")
    host: str = Field("rabbitmq", env="RABBIT_HOST")
    port: int = Field(5672, env="RABBIT_PORT")
    exchange: str = Field("", env="RABBIT_EXCHANGE")
    queue: str = Field("", env="QUEUE")


class Gunicorn(BaseSettings):
    gunicorn_bind_host: str = Field("0.0.0.0", env="GUNICORN_HOST")
    gunicorn_bind_port: str = Field("8000", env="GUNICORN_PORT")


class Settings(BaseSettings):

    log_level: int = logging.DEBUG
    logging_config: dict = LOGGING

    project_name: str = Field("RabbitService", env="PROJECT_NAME")

    postgres_settings = Postgres()
    rabbit_settings = RabbitMQ()
    gunicorn_settings = Gunicorn()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


settings = Settings(_env_file=find_dotenv(), _env_file_encoding="utf-8")


class Queue(Enum):
    fast = True
    slow = False
