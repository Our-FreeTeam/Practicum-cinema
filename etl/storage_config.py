from typing import Optional

from pydantic import BaseSettings, Field


class StorageSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PGDB(StorageSettings):
    dbname: str = Field(..., env="DB_NAME")
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    host: Optional[str] = Field(..., env="DB_HOST")
    port: int = Field(..., env="DB_PORT")


class ESHost(StorageSettings):
    hosts: str = Field(..., env="ELASTIC_URL")


class Settings(StorageSettings):
    load_delay: int = Field(..., env='LOAD_DELAY')
    batch_size: int = Field(..., env='BATCH_SIZE')
    max_modified_retries_count: int = Field(..., env='MAX_MODIFIED_RETRIES_COUNT')

    log_format: str = Field(..., env='LOG_FORMAT')
    log_level: int = Field(..., env='LOG_LEVEL')

    dbservice: str = Field(..., env='DB_SERVICE')

    uploaded_index: str = Field(..., env='UPLOADED_INDEX')


pgdb = PGDB()
es_host = ESHost()
settings = Settings()
