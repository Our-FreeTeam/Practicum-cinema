from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mongodb_url: str = Field(..., env='MONGODB_URL')
    mongodb_host: str = Field(..., env='MONGODB_HOST')
    mongodb_port: str = Field(..., env='MONGODB_PORT')

    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    auth_url: str = Field(..., env='AUTH_URL')

    request_timeout: int = Field(..., env='REQUEST_TIMEOUT')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
