import pytest
from helpers import make_get_request


@pytest.mark.parametrize(
    'answer_code, query_data, expected_answer',
    [
        # test api /persons
        (200, '/api/v1/persons/26dcf837-0327-4777-81f0-f0a59109769c', 3),
        (200, '/api/v1/persons/2cd05c17-3956-4ceb-8d75-a88a2a0ad34b', 3),
        (404, '/api/v1/persons/8886a39b-9a9f-4b1a-b8d7-139d1f5b5a92', 1),  # Персоны с таким uuid нет
        (200, '/api/v1/persons/search?sort=uuid&page_size=999', 5),
        (200, '/api/v1/persons/search?query=Ivanov&sort=uuid&page_size=1', 1),
        (200, '/api/v1/persons/26dcf837-0327-4777-81f0-f0a59109769c/film', 1),
        (404, '/api/v1/persons/8886a39b-9a9f-4b1a-b8d7-139d1f5b5a92/film', 1)  # Персоны с таким uuid нет

    ], ids=['Search for person "Ivanov" by UUID',
            'Search for genre "Petrova" by UUID',
            'Search for wrong person',
            'Show all persons',
            'Search for person "Ivanov" by Last name',
            'Search for persons (Ivanov) films by UUID',
            "Search for wrong person's films",
            ]
)
@pytest.mark.asyncio
async def test_search(es_prepare_test_data, query_data, expected_answer, answer_code: int):
    result_body = await make_get_request(query_data, "", answer_code)
    body = result_body.get('result_list')
    result_len = len(result_body if body is None else body)

    assert result_len == expected_answer
