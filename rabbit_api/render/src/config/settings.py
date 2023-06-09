import logging

from dotenv import find_dotenv
from pydantic import BaseSettings, Field
from logging import config as logging_config


# Применяем настройки логирования
from config.logger import LOGGING

logging_config.dictConfig(LOGGING)


class RabbitMQ(BaseSettings):
    username: str = Field("guest", env="RABBIT_USER")
    password: str = Field("password", env="RABBIT_PASSWORD")
    host: str = Field("rabbitmq", env="RABBIT_HOST")
    port: str = Field("5672", env="RABBIT_PORT")
    exchange: str = Field("", env="RABBIT_EXCHANGE")
    queue: str = Field("", env="QUEUE")


class Auth(BaseSettings):
    url: str = Field("guest", env="AUTH_URL")
    authorization: str = Field("password", env="AUTH_AUTHORIZATION")


class Bitly(BaseSettings):
    endpoint: str = 'https://api-ssl.bitly.com/v4/shorten'
    access_token: str = Field(None, env="BITLY_ACCESS_TOKEN")


class Settings(BaseSettings):

    log_level: int = logging.DEBUG
    logging_config: dict = LOGGING

    project_name: str = Field("RabbitService", env="PROJECT_NAME")

    rabbit_settings = RabbitMQ()
    auth_settings = Auth()
    bitly_settings = Bitly()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


settings = Settings(_env_file=find_dotenv(), _env_file_encoding="utf-8")
