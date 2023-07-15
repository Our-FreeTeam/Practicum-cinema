from functools import wraps
from http import HTTPStatus
from uuid import UUID

import aiohttp
import requests
from fastapi import HTTPException

from core.config import settings
from utils import backoff


async def update_subscription_role(user_id: UUID, role_name: str = 'Subscriber'):
    async with aiohttp.ClientSession() as session:
        token_headers = await get_token(session)
        await grant_role(session, user_id, role_name, token_headers)


async def get_token(session):
    auth_url = settings.auth_url
    async with session.post(
            f'{auth_url}v1/auth/login',
            json={"user": settings.auth_user, "password": settings.auth_password}) as token:
        headers = {}
        if (token.headers.get("access_token") is not None and
                token.headers.get("refresh_token") is not None):
            headers['access_token'] = token.headers.get("access_token")
            headers['refresh_token'] = token.headers.get("refresh_token")
        return headers


async def grant_role(user_id: UUID, role_name: str, session: aiohttp.ClientSession, headers: dict):
    auth_url = settings.auth_url
    async with session.post(
            f'{auth_url}v1/admin/grant_role_by_id',
            json={"user_id": user_id, "role_name": role_name},
            headers=headers
    ) as response:
        if response.status != 200:
            raise HTTPException(status_code=response.status,
                                detail=await response.text())


def is_authorized(func):
    @wraps(func)
    async def inner(*args, **kwargs):  # noqa: WPS430
        request = kwargs.get('request')
        if request:
            headers = request.headers
            tokens = {
                'access_token': headers.get('access_token'),
                'refresh_token': headers.get('refresh_token'),
            }
            dict_keys = list(kwargs.keys())
            dict_keys.remove('request')

            user = kwargs.get('user_id')
            get_user_id = user if user else kwargs[dict_keys[0]].user_id
            if tokens['access_token']:
                return await request_auth(*args, exec_func=func, tokens=tokens, get_user_id=get_user_id, **kwargs)
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=messages.INCORRECT_TOKEN,
        )
    return inner


@backoff.on_exception(  # noqa: WPS317
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    max_tries=8,
    jitter=None,
)
async def request_auth(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{settings.auth_url}v1/admin/user/{kwargs.pop("get_user_id")}/check_authorization',
            headers={'Content-Type': 'application/json'} | kwargs.pop('tokens'),
        ) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(
                    status_code=response.status,
                    detail=await response.text(),
                )
            exec_func = kwargs.pop('exec_func')
            return await exec_func(*args, **kwargs)