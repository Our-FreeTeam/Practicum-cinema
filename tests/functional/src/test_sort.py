import pytest
from helpers import make_get_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code,api,sort_query,expected_zero_element',
    [(200, '/api/v1/genres', {'sort': 'uuid'}, '0402143a-19a9-495d-9cca-e65e9e5e4509'),
     (200, '/api/v1/genres', {'sort': '-uuid'}, 'e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a'),
     (200, '/api/v1/persons/search', {'sort': 'uuid'}, '26dcf837-0327-4777-81f0-f0a59109769c'),
     (200, '/api/v1/persons/search', {'sort': '-uuid'}, 'ec64d43b-806d-42b6-99c9-9c4b89cdcebf'),
     (200, '/api/v1/films', {'sort': 'uuid'}, '70a6ed85-6fa1-4ec7-a6bb-5b1f2670c0a3'),
     (200, '/api/v1/films', {'sort': '-uuid'}, 'b34e2bcf-2591-4cf8-a921-28b9f276b14c'),
     (200, '/api/v1/films', {'sort': 'imdb_rating'}, '7bdfaf70-2f7a-4392-9986-c8e6aa88d6e4'),
     (200, '/api/v1/films', {'sort': '-imdb_rating'}, 'b34e2bcf-2591-4cf8-a921-28b9f276b14c'),
     (200, '/api/v1/films/search', {'sort': 'uuid'}, '70a6ed85-6fa1-4ec7-a6bb-5b1f2670c0a3'),
     (200, '/api/v1/films/search', {'sort': '-uuid'}, 'b34e2bcf-2591-4cf8-a921-28b9f276b14c'),
     (200, '/api/v1/films/search', {'sort': 'imdb_rating'}, '7bdfaf70-2f7a-4392-9986-c8e6aa88d6e4'),
     (200, '/api/v1/films/search', {'sort': '-imdb_rating'}, 'b34e2bcf-2591-4cf8-a921-28b9f276b14c'),
     ])
async def test_sort(es_prepare_test_data, api: str, sort_query: str, expected_zero_element: str, answer_code: int):
    response_body = await make_get_request(api, sort_query, answer_code)
    first_value = response_body.get('result_list') or None
    if first_value:
        first_value = first_value[0].get('uuid')
    assert first_value == expected_zero_element
