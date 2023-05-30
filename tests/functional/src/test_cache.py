import pytest
import hashlib
from helpers import make_get_request

from settings import test_settings


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code,type,api,sort_query',
    [(200, 'list', '/api/v1/genres', {'sort': 'uuid'}),
     (200, 'item', '/api/v1/genres/5b73b2c3-dac0-4c48-b917-a8efba4b3456', {}),
     (200, 'list', '/api/v1/persons/search', {'sort': '-uuid'}),
     (200, 'item', '/api/v1/persons/c177c3d5-b562-410d-931c-702f69fbb638', {}),
     (200, 'item', '/api/v1/persons/c177c3d5-b562-410d-931c-702f69fbb638/film', {}),
     (200, 'list', '/api/v1/films', {'sort': 'imdb_rating'}),
     (200, 'item', '/api/v1/films/70a6ed85-6fa1-4ec7-a6bb-5b1f2670c0a3', {}),
     (200, 'list', '/api/v1/films/search', {'query': 'Gone of the wind'}),
     ])
async def test_cache(clear_redis_cache, es_prepare_test_data, redis_client, type: str, api: str, sort_query: dict,
                     answer_code: int):
    async def get_cache(type, api, sort_query, redis_client):
        if type == 'list':
            index_name = api.replace('/api/v1/', '').replace('/search', '')
            redis_hash = f"{index_name}{sort_query.get('sort', 'uuid')}" \
                         f"{sort_query.get('page_size', test_settings.page_size)}" \
                         f"{sort_query.get('last_element', None)}{sort_query.get('genre', None)}" \
                         f"{sort_query.get('query', None)}"
            redis_hash = hashlib.md5(redis_hash.encode()).hexdigest()
        else:
            redis_hash = hashlib.md5(str(api.split('/')[4]).encode()).hexdigest()
        return await redis_client.get(redis_hash)

    assert not bool(await get_cache(type, api, sort_query, redis_client))

    await make_get_request(api, sort_query, answer_code)

    assert bool(await get_cache(type, api, sort_query, redis_client))
