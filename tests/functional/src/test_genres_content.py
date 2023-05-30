import pytest
from helpers import make_get_request


@pytest.mark.parametrize(
    'answer_code, query_data, expected_answer',
    [
        # test api /genres
        (200, '/api/v1/genres/5b73b2c3-dac0-4c48-b917-a8efba4b3456', 4),
        (200, '/api/v1/genres/5b73b2c3-dac0-4c48-b917-a8efba4b3456', 4),
        (200, '/api/v1/genres/', 5),
        (404, '/api/v1/genres/8886a39b-9a9f-4b1a-b8d7-139d1f5b5a92', 1),  # Жанрв с таким uuid нет
    ], ids=['Search for genre "Multiplication" by UUID',
            'Search for genre "Multiplication" by UUID from cache',
            'Show all genres from ES',
            'Search for wrong genre'
            ]
)
@pytest.mark.asyncio
async def test_search(es_prepare_test_data, query_data, expected_answer, answer_code):
    result_body = await make_get_request(query_data, "", answer_code)
    body = result_body.get('result_list')
    result_len = len(result_body if body is None else body)

    assert result_len == expected_answer
