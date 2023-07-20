from http import HTTPStatus

import pytest
import requests

from tests_billing.settings import settings
from tests_billing.functional.utils.helpers import HEADERS

sub_url = settings.subscription_url
headers = HEADERS
keycloak_url = settings.keycloak_url


@pytest.mark.asyncio
async def test_get_subscription_statistic(
        create_test_user_and_role
):
    site_url = settings.auth_url

    # логирование админа
    api_url = "v1/auth/login"
    body = {"user": "cinema_admin", "password": "password"}
    url_params = {
        "url": site_url + api_url,
        "json": body,
        "headers": headers
    }
    result = requests.post(**url_params)
    if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
        headers["access_token"] = result.headers.get("access_token")
        headers["refresh_token"] = result.headers.get("refresh_token")
    assert result.status_code == HTTPStatus.OK

    # выдача роли statistic_manager
    api_url = "v1/admin/grant_role"
    body = {"user_name": "cinema_admin", "role_name": "statistic_manager"}
    url_params = {
        "url": site_url + api_url,
        "json": body,
        "headers": headers
    }
    result = requests.post(**url_params)
    if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
        headers["access_token"] = result.headers.get("access_token")
        headers["refresh_token"] = result.headers.get("refresh_token")
    assert result.status_code == HTTPStatus.OK

    body_get = {
        "start_date": "2022-11-16 20:14:09.313290",
        "is_active": True,
        "order_by": "start_date",
        "page": 1,
        "size": 50
    }
    # запрос по статистике подписок
    url = f"api/v1/statistics/subscriptions"
    response = requests.get(sub_url + url, json=body_get, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["items"]) > 0

    body = {
        "payment_amount": 1000.00,
        "order_by": "payment_date",
        "page": 1,
        "size": 50
    }
    # запрос по статистике платежей
    url = f"api/v1/statistics/payments"
    response = requests.get(sub_url + url, json=body, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["items"]) > 0

    # удаление тестовой роли админа
    api_url = "v1/admin/revoke_role"
    body = {"user_name": "cinema_admin", "role_name": "statistic_manager"}
    url_params = {
        "url": site_url + api_url,
        "json": body,
        "headers": headers
    }
    result = requests.post(**url_params)
    if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
        headers["access_token"] = result.headers.get("access_token")
        headers["refresh_token"] = result.headers.get("refresh_token")
    assert result.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_fail_get_statistic():
    body_get = {
        "start_date": "2022-11-16 20:14:09.313290",
        "is_active": True,
        "order_by": "start_date",
        "page": 1,
        "size": 50
    }
    # запрос по статистике подписок
    url = f"api/v1/statistics/subscriptions"
    response = requests.get(sub_url + url, json=body_get)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    body = {
        "payment_amount": 1000.00,
        "order_by": "payment_date",
        "page": 1,
        "size": 50
    }
    # запрос по статистике платежей
    url = f"api/v1/statistics/payments"
    response = requests.get(sub_url + url, json=body)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
