import pytest
from helpers import make_get_request


@pytest.mark.parametrize(
    'answer_code, query_data, expected_answer',
    [
        # test api /films
        (200, '/api/v1/films/b34e2bcf-2591-4cf8-a921-28b9f276b14c', 8),
        (200, '/api/v1/films/b34e2bcf-2591-4cf8-a921-28b9f276b14c', 8),
        (200, '/api/v1/films/', 5),
        (404, '/api/v1/films/8886a39b-9a9f-4b1a-b8d7-139d1f5b5a92', 1),  # Фильма с таким uuid нет
    ], ids=['Search for "USS Callister" by UUID',
            'Search for "USS Callister" by UUID from cache',
            'Show all films from ES',
            'Search for wrong film'
            ]
)
@pytest.mark.asyncio
async def test_search(es_prepare_test_data, query_data, expected_answer, answer_code):
    result_body = await make_get_request(query_data, "", answer_code)
    body = result_body.get('result_list')
    result_len = len(result_body if body is None else body)

    assert result_len == expected_answer
