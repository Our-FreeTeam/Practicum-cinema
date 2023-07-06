import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    redis_cache_enabled: bool = Field(..., env='REDIS_CACHE_ENABLED')
    cache_expire: int = Field(..., env='CACHE_EXPIRE')

    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(..., env='ELASTIC_PORT')

    auth_url: str = Field(..., env='AUTH_URL')

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    page_size: int = Field(..., env='PAGE_SIZE')

    helios_api_token: str = Field(..., env='HELIOS_API_TOKEN')
    helios_enabled: bool = Field(..., env='HELIOS_ENABLED')

    recapcha_api_key: str = Field(..., env='RECAPCHA_API_KEY')
    recapcha_enabled: bool = Field(..., env='RECAPCHA_ENABLED')


class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'


settings = Settings()
