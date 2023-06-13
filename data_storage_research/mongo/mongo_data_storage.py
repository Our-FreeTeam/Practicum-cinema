"""Тестирование MongoDB."""
import time
from typing import Callable
from uuid import uuid4

from pymongo import MongoClient

from data_storage_research.fake_data import fake_batch, fake_users_batch
from data_storage_research.settings import settings


client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT, connect=True)
mongo_db = client[settings.MONGO_DB]


def mongo_insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = settings.ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    collection = mongo_db.get_collection(collection_name)
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, settings.USERS_IN_BATCH, batch_size)
        start = time.time()
        collection.insert_many(batch)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    return mean_batch / batch_size


def mongo_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    collection = mongo_db.get_collection(collection_name)
    users = [str(uuid4()) for _ in range(users_size)]

    batch_count = int(settings.TEST_RECORDS_SIZE / settings.OPTIMAL_BATCH_SIZE)
    for i in range(batch_count):
        batch = fake_users_batch(faker, users, batch_size=settings.OPTIMAL_BATCH_SIZE)
        collection.insert_many(batch)

    for user in users:
        start = time.time()
        _ = list(collection.find({"user_id": user}))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    return mean_batch
