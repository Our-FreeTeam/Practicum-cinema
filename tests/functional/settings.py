from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    redis_cache_enabled: bool = Field(..., env='REDIS_CACHE_ENABLED')
    cache_expire: int = Field(..., env='CACHE_EXPIRE')
    elastic_url: str = Field(..., env='ELASTIC_URL')
    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(..., env='ELASTIC_PORT')

    es_index: str = "films"
    es_id_field: str = "uuid"
    es_index_mapping: dict = ""

    service_url: str = Field(..., env='FASTAPI_URL')

    page_size: int = Field(..., env='PAGE_SIZE')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


test_settings = Settings()


if __name__ == '__main__':
    pass
