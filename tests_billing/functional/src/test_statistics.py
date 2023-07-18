# import logging
# from datetime import datetime
# from http import HTTPStatus
#
# import pytest
# import requests
# from dateutil.relativedelta import relativedelta
#
# from tests_billing.settings import settings
# from tests_billing.functional.utils.helpers import get_active_subscription, HEADERS, get_payment_id, duration
#
#
# sub_url = settings.subscription_url
# headers = HEADERS
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'answer_code, req_type, api_url, body',
#     [
#         (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
#         (200, 'POST', 'v1/admin/grant_role', {"user_name": "cinema_admin", "role_name": "statistic_manager"}),
#     ],
# )
# async def test_login_and_get_role(
#         answer_code,
#         req_type,
#         api_url,
#         body,
#         create_remove_test_user_and_role,
#         get_user
# ):
#     site_url = settings.auth_url
#     url_params = {
#         "url": site_url + api_url,
#         "json": body,
#         "headers": headers
#     }
#     result = requests.post(**url_params)
#     logging.info(f"result: {result.json()}")
#     print(f"print: {result.json()}")
#     if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
#         headers["access_token"] = result.headers.get("access_token")
#         headers["refresh_token"] = result.headers.get("refresh_token")
#     assert result.status_code == answer_code
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'answer_code, req_type, api_url, body',
#     [
#         (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
#     ],
# )
# async def test_check_subscriptions_statistic(
#         answer_code,
#         req_type,
#         api_url,
#         body,
#         create_remove_test_user_and_role,
#         get_user
# ):
#     site_url = settings.auth_url
#     url_params = {
#         "url": site_url + api_url,
#         "json": body,
#         "headers": headers
#     }
#     result = requests.post(**url_params)
#     if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
#         headers["access_token"] = result.headers.get("access_token")
#         headers["refresh_token"] = result.headers.get("refresh_token")
#     assert result.status_code == answer_code
#
#     sub_body = {
#         "is_active": True
#     }
#     url = "api/v1/statistics/subscriptions"
#     response = requests.post(sub_url + url, json=sub_body)
#     assert response.status_code == answer_code
#     assert response.json() == ''
