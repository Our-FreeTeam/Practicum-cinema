# import pytest
# import requests
#
# from tests_billing.settings import settings
# from tests_billing.functional.utils.helpers import HEADERS
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
#         (200, 'POST', 'v1/admin/grant_role', {"user_name": "test_user", "role_name": "statistic_manager"}),
#     ],
# )
# @pytest.mark.asyncio
# async def test_get_subscription_statistic(
#         answer_code,
#         req_type,
#         api_url,
#         body,
#         create_remove_test_user_and_role
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
#     body = {
#         "start_date": "2022-11-16 20:14:09.313290",
#         "is_active": True,
#         "order_by": "start_date",
#         "page": 1,
#         "size": 50
#     }
#     url = f"api/v1/statistics/subscriptions"
#     response = requests.get(sub_url + url, json=body, headers=result.headers)
#     assert response.status_code == answer_code
#     assert len(response.json()["items"]) > 0
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     'answer_code, req_type, api_url, body',
#     [
#         (200, 'POST', 'v1/auth/login', {"user": "cinema_admin", "password": "password"}),
#         (200, 'POST', 'v1/admin/grant_role', {"user_name": "test_user", "role_name": "statistic_manager"}),
#     ],
# )
# @pytest.mark.asyncio
# async def test_get_payment_statistic(
#         answer_code,
#         req_type,
#         api_url,
#         body,
#         create_remove_test_user_and_role
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
#     body = {
#         "payment_amount": 1000.00,
#         "order_by": "payment_date",
#         "page": 1,
#         "size": 50
#     }
#     url = f"api/v1/statistics/payments"
#     response = requests.get(sub_url + url, json=body, headers=result.headers)
#     assert response.status_code == answer_code
#     assert len(response.json()["items"]) > 0
