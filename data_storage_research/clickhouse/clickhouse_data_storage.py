"""Тестовая загрузка данных в ClickHouse."""

import time
from typing import Callable
from uuid import uuid4

from data_storage_research.fake_data import fake_batch, fake_users_batch
from data_storage_research.settings import settings
from data_storage_research.clickhouse.clickhouse_adapter import adapter


def clickhouse_insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = settings.ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, settings.USERS_IN_BATCH, batch_size)
        start = time.time()
        step_data = []
        str_key = ""
        for value in batch:
            str_key = ", ".join(value.keys())
            step_data.append(tuple(value.values()))
        adapter.execute(f"""INSERT INTO {collection_name} ({str_key}) VALUES""", step_data)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    return mean_batch / batch_size


def clickhouse_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    users = [str(uuid4()) for _ in range(users_size)]

    batch_count = int(settings.TEST_RECORDS_SIZE / settings.OPTIMAL_BATCH_SIZE)
    for i in range(batch_count):
        batch = fake_users_batch(faker, users, batch_size=settings.OPTIMAL_BATCH_SIZE)
        adapter.execute(f"""INSERT INTO {collection_name} (user_id) VALUES""", batch)

    for user in users:
        start = time.time()
        _ = list(adapter.execute(f"SELECT * FROM {collection_name} WHERE user_id = '{user}'"))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    return mean_batch
