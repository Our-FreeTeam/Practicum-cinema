from http import HTTPStatus

import pytest
import requests

from core.config import settings


@pytest.mark.asyncio
async def test_create_sub_step_1():
    body_step_1 = {
        "user_id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
        "start_date": "2022-06-16 20:14:09.31329",
        "end_date": "2023-06-16 20:14:09.31329",
        "subscription_type_id": "59507685-5b50-4d60-b4d1-6fc0ab1bacd1",
        "is_active": True,
        "is_repeatable": True,
        "save_payment_method": True
    }
    url_step_1 = "api/v1/subscriptions/add_1_step"
    response = requests.post(settings.SUBSCRIPTION_URL + url_step_1, json=body_step_1)
    assert response.status_code == HTTPStatus.OK
    resp_url = response.json()["url"]
    body_step_2 = {
        "external_data": [
            {
                "url": resp_url,
                "pay_data": {
                    "event": "payment.succeeded",
                    "object": {
                        "id": "8d327690-ce91-459d-a743-ef31a15476a8",
                        "status": "succeeded",
                        "payment_method": {
                            "id": "215d8da0-000f-50be-b000-0003308c89be"
                        }
                    }
                },
            }
        ]
    }
    url_step_2 = "api/v1/subscriptions/add_2_step"
    response = requests.post(settings.SUBSCRIPTION_URL + url_step_2, json=body_step_2)
    assert response.status_code == HTTPStatus.OK
