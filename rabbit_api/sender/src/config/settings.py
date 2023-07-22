from pydantic import BaseSettings, Field


class Postgres(BaseSettings):
    # Настройки Redis
    dbname: str = Field("postgres", env="NOTIFICATION_POSTGRES_USER")
    user: str = Field("postgres", env="NOTIFICATION_POSTGRES_USER")
    password: str = Field("password", env="NOTIFICATION_POSTGRES_PASSWORD")
    host: str = Field("localhost", env="NOTIFICATION_POSTGRES_HOST")
    port: int = Field(5435, env="NOTIFICATION_POSTGRES_PORT")


class RabbitMQ(BaseSettings):
    username: str = Field("guest", env="RABBIT_USER")
    password: str = Field("guest", env="RABBIT_PASSWORD")
    host: str = Field("rabbitmq", env="RABBIT_HOST")
    port: int = Field(5672, env="RABBIT_PORT")
    exchange: str = Field("", env="RABBIT_EXCHANGE")
    queue: str = Field("sender", env="RABBIT_QUEUE")


class Sender(BaseSettings):
    address: str = Field("smtp.yandex.ru", env="SERVER_ADDRESS")
    port: int = Field(465, env="SERVER_PORT")
    login: str = Field("login", env="EMAIL_LOGIN")
    password: str = Field("password", env="EMAIL_PASSWORD")


# Загружаем настройки
email_server_settings = Sender()
postgres_settings = Postgres()
rabbit_settings = RabbitMQ()
