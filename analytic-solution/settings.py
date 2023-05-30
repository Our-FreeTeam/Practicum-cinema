from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_interface_url: str = Field(..., env='KAFKA_INTERFACE_URL')
    kafka_broker_url: str = Field(..., env='KAFKA_BROKER_URL')
    topic_name: str = Field(..., env='KAFKA_TOPIC')

    redis_host: str = Field(..., env='UGC_REDIS_HOST')
    redis_port: str = Field(..., env='UGC_REDIS_PORT')

    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    auth_url: str = Field(..., env='AUTH_URL')

    request_timeout: int = Field(..., env='REQUEST_TIMEOUT')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
