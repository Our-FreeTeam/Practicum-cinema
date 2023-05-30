import json

import pytest
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis
from settings import test_settings
from testdata.es_data_collection import test_data


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.elastic_url)
    yield client
    await client.close()


def get_es_bulk_query(data: str, es_index: str, es_id_filed: str) -> list:
    prep_query = []
    for row in data:
        prep_query.extend([
            json.dumps({'index': {'_index': es_index,
                                  '_id': row[es_id_filed]}}),
            json.dumps(row)
        ])
    return prep_query


@pytest.fixture(scope='session')
async def es_prepare_test_data(es_client):
    str_query = ''
    for index, index_value in test_data.items():
        bulk_query = get_es_bulk_query(index_value, index, test_settings.es_id_field)
        str_query += '\n'.join(bulk_query) + '\n'
    response = await es_client.bulk(body=str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')


@pytest.fixture(scope='function')
async def clear_redis_cache():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    await redis.flushall()


@pytest.fixture(scope='function')
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield client
    await client.close()
