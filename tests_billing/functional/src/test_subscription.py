import logging
from datetime import datetime
from http import HTTPStatus

import pytest
import requests

from tests_billing.settings import settings
from tests_billing.functional.utils.helpers import get_active_subscription

sub_url = settings.subscription_url


@pytest.mark.asyncio
async def test_create_and_pay_payment():
    body_step_1 = {
        "user_id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
        "start_date": "2022-06-16 20:14:09.31329",
        "end_date": "2023-06-16 20:14:09.31329",
        "subscription_type_id": "834c0eb9-7ac6-47a8-aa51-19d1f2f58766",
        "is_active": True,
        "is_repeatable": True,
        "save_payment_method": True
    }
    url_step_1 = "api/v1/subscriptions/add_1_step"
    response = requests.post(sub_url + url_step_1, json=body_step_1)
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
    response = requests.post(sub_url + url_step_2, json=body_step_2)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "body, status",
    [
        ({
             "user_id": 1,
             "start_date": "2022-06-16 20:14:09.31329",
             "end_date": "2023-06-16 20:14:09.31329",
             "subscription_type_id": "834c0eb9-7ac6-47a8-aa51-19d1f2f58766",
             "is_active": True,
             "is_repeatable": True,
             "save_payment_method": True
         }, 422),
        ({
             "user_id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
             "start_date": "2022-06-16 20:14:09.31329",
             "end_date": "2023-06-16 20:14:09.31329",
             "subscription_type_id": 1,
             "is_active": True,
             "is_repeatable": True,
             "save_payment_method": True
         }, 422),
    ]
)
@pytest.mark.asyncio
async def test_invalid_payment(body, status):
    url_step_1 = "api/v1/subscriptions/add_1_step"
    response = requests.post(sub_url + url_step_1, json=body)
    msg = response.json()["detail"][0]["msg"]
    assert response.status_code == status
    assert msg == "value is not a valid uuid"


@pytest.mark.asyncio
async def test_check_subscription():
    body = {
        "user_id": "26e83050-29ef-4163-a99d-b546cac208f8",
        "start_date": "2022-06-16 20:14:09.31329",
        "end_date": "2023-06-16 20:14:09.31329",
        "subscription_type_id": "1311e24e-a912-400b-a254-28aa45b01975",
        "is_active": False,
        "is_repeatable": True,
        "save_payment_method": True
    }
    url = "api/v1/subscriptions/add_1_step"
    response = requests.post(sub_url + url, json=body)
    msg = response.json()["detail"]
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert msg == "Не найден тип подписки"


@pytest.mark.asyncio
async def test_correct_dates():
    user_id = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    active_subscription = await get_active_subscription(user_id=user_id)
    sub_start_date = active_subscription[2]
    sub_end_date = active_subscription[3]
    assert isinstance(sub_start_date, datetime)
    assert isinstance(sub_end_date, datetime)
