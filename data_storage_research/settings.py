"""Настройки проекта."""
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Настройки."""

    LOGGING_LEVEL: str = "INFO"
    SLEEP_TIME: int = 1

    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_DATABASE: str = "test_ch"
    CLICKHOUSE_CLUSTER: str = "practicum_cluster"
    CLICKHOUSE_CLUSTER_HOST: list[str] = Field(default="clickhouse-node1, clickhouse-node3")

    SHARD_DB = "shard"
    REPLICA_DB = "replica"
    USER_CH = "ugc_user"
    PASSWORD_CH = "12345"

    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB = "ugc_db"

    DB_BACKOFF_MAX_TIME: int = 20
    DB_BACKOFF_MAX_TRIES: int = 50

    COLLECTION_LIKE = "likedFilms"
    COLLECTION_REVIEW = "reviews"
    COLLECTION_BOOKMARK = "bookmarks"

    ITERATIONS_NUMBER = 10
    USERS_IN_BATCH = 10
    OPTIMAL_BATCH_SIZE = 200
    TEST_RECORDS_SIZE = 10000

    @validator("CLICKHOUSE_CLUSTER_HOST", pre=True)
    def set_cluster_hosts(cls, value: str) -> list[str]:
        """Установка значения параметра CLICKHOUSE_CLUSTER_HOST."""
        return [item.strip() for item in value.split(",")]


settings = Settings()