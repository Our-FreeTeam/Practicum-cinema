import pytest
from helpers import make_get_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code,api,sort_query',
    [(200, '/api/v1/genres', {'sort': 'uuid'}),
     (200, '/api/v1/genres', {'sort': '-uuid'}),
     (200, '/api/v1/persons/search', {'sort': 'uuid'}),
     (200, '/api/v1/persons/search', {'sort': '-uuid'}),
     (200, '/api/v1/films', {'sort': 'uuid'}),
     (200, '/api/v1/films', {'sort': '-uuid'}),
     (200, '/api/v1/films', {'sort': 'imdb_rating'}),
     (200, '/api/v1/films', {'sort': '-imdb_rating'}),
     (200, '/api/v1/films/search', {'sort': 'uuid'}),
     (200, '/api/v1/films/search', {'sort': '-uuid'}),
     (200, '/api/v1/films/search', {'sort': 'imdb_rating'}),
     (200, '/api/v1/films/search', {'sort': '-imdb_rating'}),
     ])
async def test_get_last_element(es_prepare_test_data, api: str, sort_query: dict, answer_code: int):
    response_body = await make_get_request(api, sort_query, answer_code)
    last_element = response_body.get('last_element')
    sort_field_value = response_body.get('result_list') or None
    if sort_field_value:
        sort_field_value = sort_field_value[-1].get(sort_query['sort'].replace('-', ''))
    assert last_element == str(sort_field_value)
