from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    debug_mode: int = Field(0, env='BILLING_DEBUG')

    kafka_interface_url: str = Field(..., env='KAFKA_INTERFACE_URL')
    kafka_broker_url: str = Field(..., env='KAFKA_BROKER_URL')

    whok_topic_name: str = Field(..., env='WHOOK_TOPIC_LOG')
    success_pay_topic: str = Field(..., env='SUCCESS_PAY_LOG')
    error_pay_topic: str = Field(..., env='ERROR_PAY_LOG')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
