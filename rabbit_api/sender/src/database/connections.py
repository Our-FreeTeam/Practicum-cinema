import psycopg2
from psycopg2.extensions import connection


def create_pg_conn(dbname: str, host: str, port: int, user: str, password: str, cursor_factory) -> connection:
    """Создает подключение к Postgres"""
    pg_connection = psycopg2.connect(
            dbname=dbname,
            host=host,
            port=port,
            user=user,
            password=password,
            cursor_factory=cursor_factory
            )

    return pg_connection
