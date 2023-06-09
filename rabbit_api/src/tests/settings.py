import logging
from enum import Enum

from dotenv import find_dotenv
from pydantic import BaseSettings, Field
from logging import config as logging_config


class Test(BaseSettings):
    # Настройки тестовой БД
    test_db: str = Field("test_database", env="TEST_DB")
    test_user: str = Field("test_user", env="TEST_USER")
    test_password: str = Field("test_password", env="TEST_PASSWORD")
    test_db_port: str = Field("test_port", env="TEST_DB_PORT")
    test_db_host: str = Field("5432", env="TEST_DB_HOST")


class Postgres(BaseSettings):
    # Настройки Redis
    dbname: str = Field("events_database", env="POSTGRES_DB")
    user: str = Field(None, env="POSTGRES_USER")
    password: str = Field(None, env="POSTGRES_PASSWORD")
    host: str = Field(None, env="DB_HOST")
    port: str = Field(None, env="DB_PORT")


class RabbitMQ(BaseSettings):
    username: str = Field("guest", env="RABBIT_USER")
    password: str = Field("password", env="RABBIT_PASSWORD")
    host: str = Field("rabbitmq", env="RABBIT_HOST")
    port: str = Field("5672", env="RABBIT_PORT")
    exchange: str = Field("", env="RABBIT_EXCHANGE")
    queue: str = Field("", env="QUEUE")


class Sender(BaseSettings):
    server_adress: str = Field("smtp.yandex.ru", env="SERVER_ADDRESS")
    server_port: str = Field("465", env="SERVER_PORT")
    email_login: str = Field("test", env="EMAIL_LOGIN")
    email_password: str = Field("test", env="EMAIL_PASSWORD")


class Gunicorn(BaseSettings):
    gunicorn_bind_host: str = Field("localhost", env="GUNICORN_HOST")
    gunicorn_bind_port: str = Field("8000", env="GUNICORN_PORT")


class Settings(BaseSettings):
    client_id: str = Field(None, env="CLIENT_ID")
    client_secret: str = Field(None, env="CLIENT_SECRET")

    log_level: int = logging.DEBUG

    project_name: str = Field("RabbitService", env="PROJECT_NAME")

    email_server_settings = Sender()
    postgres_settings = Postgres()
    rabbit_settings = RabbitMQ()
    gunicorn_settings = Gunicorn()
    test_settings = Test()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


settings = Settings(_env_file=find_dotenv(), _env_file_encoding="utf-8")


class Queue(Enum):
    fast = True
    slow = False
