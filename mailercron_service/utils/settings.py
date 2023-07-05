from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    realm_name: str = Field(..., env='KEYCLOAK_REALM_ID')
    client_secret_key: str = Field(..., env='KEYCLOAK_SECRET_KEY')
    service_account: str = Field(..., env='KEYCLOAK_SERVICE_ACCOUNT')

    keycloak_admin_login: str = Field(..., env='KEYCLOAK_ADMIN')
    keycloak_admin_password: str = Field(..., env='KEYCLOAK_ADMIN_PASSWORD')
    keycloak_service_email: str = Field(..., env='KEYCLOAK_SERVICE_EMAIL')
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    keycloak_realm_su: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    keycloak_realm_su_psw: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU_PSW')

    # RabbitMQ connection parameters
    rabbitmq_user: str = Field(..., env='RABBIT_USER')
    rabbitmq_password: str = Field(..., env='RABBIT_PASSWORD')
    rabbitmq_host: str = Field(..., env='RABBIT_HOST')
    rabbitmq_port: int = Field(..., env='RABBIT_PORT')
    rabbitmq_exchange = 'delayed_exchange'
    rabbitmq_raw_queue: str = Field(..., env='RABBIT_QUEUE')
    rabbitmq_subscription_queue: str = Field(..., env='RABBIT_SUBSCRIPTION_QUEUE')

    rabbitmq_full_exchange = 'full_exchange'
    rabbitmq_full_queue: str = Field(..., env='RABBIT_FULL_QUEUE')

    rabbit_api_host: str = Field(..., env='NOTIFICATION_GUNICORN_HOST')
    rabbit_api_port: str = Field(..., env='NOTIFICATION_GUNICORN_PORT')

    ugc_api_service: str = Field(..., env='UGC_API_URL')
    auth_url: str = Field(..., env='AUTH_URL')

    debug_mode: int = Field(0, env='MAILCRON_DEBUG')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
