import pytest
from helpers import make_get_request


@pytest.mark.parametrize(
    'answer_code, query_data, expected_answer',
    [
        # tests api films/search
        (200, {'query': 'Clark Gable'}, 1),
        (200, {'query': 'Gone of the wind'}, 1),
        (200, {'query': 'Vivien Leigh'}, 1,),
        (200, {'query': 'Mashed potato'}, 0),
        (200, {'query': ''}, 5),
        (200, {'query': '', 'page_size': '2'}, 2)

    ], ids=['Search for "Clark Gable" actor', 'Search for "Gone of the wind" from API',
            'Search for "Vivien Leigh"', 'Search for "Mashed potato"',
            'Search for ""', 'Search for all data with 2 elem per page'
            ]
)
@pytest.mark.asyncio
async def test_search(es_prepare_test_data, query_data, expected_answer, answer_code):
    result_body = await make_get_request('/api/v1/films/search', query_data, answer_code)
    body = result_body.get('result_list')
    result_len = len(result_body if body is None else body)

    assert result_len == expected_answer
