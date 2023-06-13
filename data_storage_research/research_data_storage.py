from typing import Callable
from matplotlib import pyplot as plt
import numpy as np

from data_storage_research.clickhouse.clickhouse_data_storage import clickhouse_insert_step, clickhouse_read_data
from data_storage_research.fake_data import fake_bookmark_event, fake_like_event, fake_review_event
from data_storage_research.mongo.mongo_data_storage import mongo_insert_step, mongo_read_data
from data_storage_research.settings import settings


def test_insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    res_mongo = []
    res_clickhouse = []
    for batch_size in batch_sizes:
        res_mongo.append(mongo_insert_step(faker, collection_name, batch_size))
        res_clickhouse.append(clickhouse_insert_step(faker, collection_name, batch_size))
    plt.plot(batch_sizes, res_mongo, color='orange', label='mongo')
    plt.plot(batch_sizes, res_clickhouse, color='blue', label='clickhouse')
    plt.title(f'Insert data of {collection_name}')
    plt.yscale('log')
    plt.show()


def test_read(read_params: list[Callable, str]) -> None:
    """Тестирование вставки с разным размером батча."""
    res_mongo = []
    res_clickhouse = []
    for read_param in read_params:
        res_mongo.append(mongo_read_data(*read_param, 20))
        res_clickhouse.append(clickhouse_read_data(*read_param, 20))

    barWidth = 0.25

    br1 = np.arange(len(res_mongo))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, res_mongo, color='orange', width=barWidth, label='Mongo')
    plt.bar(br2, res_clickhouse, color='blue', width=barWidth, label='ClickHouse')

    plt.title('Result')
    plt.xlabel('Data')
    plt.ylabel('Reading speed')

    plt.xticks([r + barWidth for r in range(len(res_mongo))],
               ['Likes', 'Review', 'Bookmark'])

    plt.legend()
    plt.show()


if __name__ == "__main__":
    test_insert(fake_like_event, settings.COLLECTION_LIKE)
    test_insert(fake_review_event, settings.COLLECTION_REVIEW)
    test_insert(fake_bookmark_event, settings.COLLECTION_BOOKMARK)

    test_read([[fake_like_event, settings.COLLECTION_LIKE],
               [fake_review_event, settings.COLLECTION_REVIEW],
               [fake_bookmark_event, settings.COLLECTION_BOOKMARK]])
