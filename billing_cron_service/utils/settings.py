from typing import Optional

from pydantic import BaseSettings, Field


class PGDB(BaseSettings):
    dbname: str = Field(..., env="BILL_DB_NAME")
    user: str = Field(..., env="BILL_DB_USERNAME")
    password: str = Field(..., env="BILL_DB_PASSWORD")
    host: Optional[str] = Field(..., env="BILL_DB_HOST")
    port: int = Field(..., env="BILL_DB_PORT")


class Settings(BaseSettings):
    keycloak_url: str = Field(..., env='KEYCLOAK_URL')
    client_id: str = Field(..., env='KEYCLOAK_CLIENT_ID')
    realm_name: str = Field(..., env='KEYCLOAK_REALM_ID')
    client_secret_key: str = Field(..., env='KEYCLOAK_SECRET_KEY')
    service_account: str = Field(..., env='KEYCLOAK_SERVICE_ACCOUNT')

    keycloak_admin_login: str = Field(..., env='KEYCLOAK_ADMIN')
    keycloak_admin_password: str = Field(..., env='KK_ADMIN_PASSWORD')
    keycloak_service_email: str = Field(..., env='KEYCLOAK_SERVICE_EMAIL')

    kafka_interface_url: str = Field(..., env='KAFKA_INTERFACE_URL')
    kafka_broker_url: str = Field(..., env='KAFKA_BROKER_URL')
    topic_name: str = Field(..., env='WHOOK_TOPIC_LOG')
    success_pay_topic: str = Field(..., env='SUCCESS_PAY_LOG')
    notif_pay_topic: str = Field(..., env='NOTIF_PAY_LOG')
    error_pay_topic: str = Field(..., env='ERROR_PAY_LOG')


    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    keycloak_realm_su: str = Field(..., env='KEYCLOAK_CINEMAREALM_SU')
    keycloak_realm_su_psw: str = Field(..., env='KK_CINEMAREALM_SU_PSW')

    debug_mode: int = Field(0, env='BILLING_DEBUG')

    rabbitmq_user: str = Field(..., env='RABBIT_USER')
    rabbitmq_password: str = Field(..., env='RABBIT_PASSWORD')
    rabbitmq_host: str = Field(..., env='RABBIT_HOST')
    rabbitmq_port: int = Field(..., env='RABBIT_PORT')
    rabbitmq_subscription_queue: str = Field(..., env='RABBIT_SUBSCRIPTION_QUEUE')

    rabbitmq_exchange = 'delayed_exchange'
    rabbitmq_queue_name: str = Field(..., env='RABBIT_SUBSCRIPTION_QUEUE')

    rabbit_api_host: str = Field(..., env='NOTIFICATION_GUNICORN_HOST')
    rabbit_api_port: str = Field(..., env='NOTIFICATION_GUNICORN_PORT')

    KASSA_ACCOUNT_ID: str = Field(..., env='KASSA_ACCOUNT_ID')
    KASSA_SECRET_KEY: str = Field(..., env='KASSA_SECRET_KEY')

    CONFIRMATION_URL: str = Field(..., env='CONFIRMATION_URL')

    billing_service_url: str = Field(..., env='BILLING_SERVICE_URL')

    redis_host: str = Field(..., env='REDIS_BILLING_HOST')
    redis_port: int = Field(..., env='REDIS_BILLING_PORT')

    auth_url: str = Field(..., env='AUTH_URL')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
pgdb = PGDB()
