from http import HTTPStatus

import aiohttp
import pytest
from fastapi.testclient import TestClient

from core.config import settings
from main import app

client = TestClient(app)


async def make_get_request(url: str, json: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.service_url + url, json=json) as response:
            return await response.json()


@pytest.mark.asyncio
async def test_create_sub_step_1():
    body = {
        "user_id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
        "start_date": "2022-06-16 20:14:09.31329",
        "end_date": "2023-06-16 20:14:09.31329",
        "subscription_type_id": "59507685-5b50-4d60-b4d1-6fc0ab1bacd1",
        "is_active": True,
        "is_repeatable": True,
        "save_payment_method": True
    }
    url = 'api/v1/subscriptions/add_1_step'
    # response = await make_get_request(url="api/v1/subscriptions/add_1_step", json=body)
    c = 1
    response = client.post("api/v1/subscriptions/add_1_step", json=body)
    assert response.status_code == HTTPStatus.OK
