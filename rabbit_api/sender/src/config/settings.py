import logging

from dotenv import find_dotenv
from pydantic import BaseSettings, Field
from logging import config as logging_config


# Применяем настройки логирования
from config.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Postgres(BaseSettings):
    # Настройки Redis
    dbname: str = Field("notifications", env="POSTGRES_DB")
    user: str = Field("admin", env="POSTGRES_USER")
    password: str = Field("123qwe", env="POSTGRES_PASSWORD")
    host: str = Field("localhost", env="POSTGRES_HOST")
    port: int = Field(5432, env="POSTGRES_PORT")


class RabbitMQ(BaseSettings):
    username: str = Field("guest", env="RABBIT_USER")
    password: str = Field("guest", env="RABBIT_PASSWORD")
    host: str = Field("rabbitmq", env="RABBIT_HOST")
    port: int = Field(5672, env="RABBIT_PORT")
    exchange: str = Field("", env="RABBIT_EXCHANGE")
    queue: str = Field("sender", env="QUEUE")


class Sender(BaseSettings):
    address: str = Field("smtp.yandex.ru", env="SERVER_ADDRESS")
    port: int = Field(465, env="SERVER_PORT")
    login: str = Field(..., env="EMAIL_LOGIN")
    password: str = Field(..., env="EMAIL_PASSWORD")


class Settings(BaseSettings):

    log_level: int = logging.DEBUG
    logging_config: dict = LOGGING

    project_name: str = Field("RabbitService", env="PROJECT_NAME")

    email_server_settings = Sender()
    postgres_settings = Postgres()
    rabbit_settings = RabbitMQ()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


settings = Settings(_env_file=find_dotenv(), _env_file_encoding="utf-8")
