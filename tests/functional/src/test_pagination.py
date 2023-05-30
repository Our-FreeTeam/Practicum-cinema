import pytest

from helpers import make_get_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer_code,api,query,expected_res',
    [(200, '/api/v1/genres', {'page_size': 100, 'last_element': ''}, 5),
     (422, '/api/v1/genres', {'page_size': 0, 'last_element': ''}, 'value_error.number.not_gt'),
     (422, '/api/v1/genres', {'page_size': -5, 'last_element': ''}, 'value_error.number.not_gt'),
     (200, '/api/v1/genres', {'page_size': 2, 'last_element': ''}, 2),
     (200, '/api/v1/genres', {'page_size': 2, 'last_element': 'e0bd70aa-0f1b-4ce7-bd87-cbf582a6dc5a'}, 0),
     (200, '/api/v1/persons/search', {'page_size': 100, 'last_element': ''}, 5),
     (422, '/api/v1/persons/search', {'page_size': 0, 'last_element': ''}, 'value_error.number.not_gt'),
     (422, '/api/v1/persons/search', {'page_size': -5, 'last_element': ''}, 'value_error.number.not_gt'),
     (200, '/api/v1/persons/search', {'page_size': 2, 'last_element': ''}, 2),
     (200, '/api/v1/persons/search', {'page_size': 2, 'last_element': 'eae29d9d-5248-45fa-9cfd-fa9a03e8d0f2'}, 1),
     (200, '/api/v1/films', {'page_size': 100, 'last_element': ''}, 5),
     (422, '/api/v1/films', {'page_size': 0, 'last_element': ''}, 'value_error.number.not_gt'),
     (422, '/api/v1/films', {'page_size': -5, 'last_element': ''}, 'value_error.number.not_gt'),
     (200, '/api/v1/films', {'page_size': 2, 'last_element': ''}, 2),
     (200, '/api/v1/films', {'page_size': 2, 'sort': 'imdb_rating', 'last_element': 8.1}, 1),
     (200, '/api/v1/films/search', {'page_size': 100, 'last_element': ''}, 5),
     (422, '/api/v1/films/search', {'page_size': 0, 'last_element': ''}, 'value_error.number.not_gt'),
     (422, '/api/v1/films/search', {'page_size': -5, 'last_element': ''}, 'value_error.number.not_gt'),
     (200, '/api/v1/films/search', {'page_size': 2, 'last_element': ''}, 2),
     (200, '/api/v1/films/search', {'page_size': 2, 'sort': 'imdb_rating', 'last_element': 8.1}, 1),
     ])
async def test_pagination(es_prepare_test_data, api: str, query: dict, expected_res: str | int, answer_code: int):
    response_body = await make_get_request(api, query, answer_code)
    el_count = response_body.get('result_list')
    if el_count is not None:
        el_count = len(el_count)
        assert el_count == expected_res
    else:
        assert response_body['detail'][0]['type'] == expected_res
