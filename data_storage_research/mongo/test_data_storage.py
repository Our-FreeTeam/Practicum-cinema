"""Тестирование MongoDB."""
import time
from typing import Callable
from uuid import uuid4

from pymongo import MongoClient
from matplotlib import pyplot as plt

from data_storage_research.fake_data import fake_batch, fake_bookmark_event, fake_like_event, fake_review_event, fake_users_batch

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB = "ugc_db"
MONGO_COLLECTION_LIKE = "likedFilms"
MONGO_COLLECTION_REVIEW = "reviews"
MONGO_COLLECTION_BOOKMARK = "bookmarks"
ITERATIONS_NUMBER = 10
USERS_IN_BATCH = 10
OPTIMAL_BATCH_SIZE = 200
TEST_RECORDS_SIZE = 10000

client = MongoClient(MONGO_HOST, MONGO_PORT, connect=True)
mongo_db = client[MONGO_DB]


def test_insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    collection = mongo_db.get_collection(collection_name)
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, USERS_IN_BATCH, batch_size)
        start = time.time()
        collection.insert_many(batch)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    return mean_batch / batch_size


def test_insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    res = []
    for batch_size in batch_sizes:
        res.append(test_insert_step(faker, collection_name, batch_size))
    plt.plot(batch_sizes, res)
    plt.title(f'Insert data of {collection_name}')
    plt.yscale('log')
    plt.show()


def test_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    collection = mongo_db.get_collection(collection_name)
    users = [str(uuid4()) for _ in range(users_size)]

    batch_count = int(TEST_RECORDS_SIZE / OPTIMAL_BATCH_SIZE)
    for i in range(batch_count):
        batch = fake_users_batch(faker, users, batch_size=OPTIMAL_BATCH_SIZE)
        collection.insert_many(batch)

    for user in users:
        start = time.time()
        _ = list(collection.find({"user_id": user}))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    return mean_batch


if __name__ == "__main__":
    test_insert(
        fake_like_event,
        MONGO_COLLECTION_LIKE,
    )

    test_insert(
        fake_review_event,
        MONGO_COLLECTION_REVIEW,
    )

    test_insert(
        fake_bookmark_event,
        MONGO_COLLECTION_BOOKMARK,
    )

    read_data_result = [test_read_data(fake_like_event, MONGO_COLLECTION_LIKE, 20),
                        test_read_data(fake_review_event, MONGO_COLLECTION_REVIEW, 20),
                        test_read_data(fake_bookmark_event, MONGO_COLLECTION_BOOKMARK, 20)]

    read_data_names = ['Mongo likes', 'Mongo review', 'Mongo bookmark']
    plt.bar(read_data_names, read_data_result, color='blue')
    plt.title('Result')
    plt.xlabel('Data')
    plt.ylabel('Reading speed')
    plt.show()
