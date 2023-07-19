from functools import wraps
from http import HTTPStatus
from uuid import UUID

import aiohttp
import requests
from fastapi import HTTPException

from core import messages
from core.config import settings
import backoff


async def update_subscription_role(user_id: UUID, role_name: str = 'subscriber'):
    async with aiohttp.ClientSession() as session:
        token_headers = await get_token(session)
        await grant_role(user_id, role_name, session, token_headers)


async def get_token(session):
    async with session.post(
            f'{settings.AUTH_URL}v1/auth/login',
            json={"user": settings.AUTH_USER, "password": settings.AUTH_PASSWORD}) as token:
        headers = {}
        if (token.headers.get("access_token") is not None and token.headers.get("refresh_token") is not None):
            headers['access_token'] = token.headers.get("access_token")
            headers['refresh_token'] = token.headers.get("refresh_token")
        return headers


async def grant_role(user_id: UUID, role_name: str, session: aiohttp.ClientSession, headers: dict):
    async with session.post(
            f'{settings.AUTH_URL}v1/admin/grant_role_by_id',
            json={"user_id": str(user_id), "role_name": role_name},
            headers=headers
    ) as response:
        if response.status != 200:
            raise HTTPException(status_code=response.status,
                                detail=await response.text())


# Декоратор для проверки токена и получения user_id
def get_user_id(func):
    @wraps(func)
    async def inner(*args, **kwargs):  # noqa: WPS430
        request = kwargs.get('request')
        if request:
            headers = request.headers
            tokens = {
                'access_token': headers.get('access_token'),
                'refresh_token': headers.get('refresh_token'),
            }
            if tokens['access_token']:
                return await request_auth(*args, exec_func=func, tokens=tokens, **kwargs)
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=messages.AUTH_ERROR,
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
            f'{settings.AUTH_URL}v1/admin/get_user_id_by_token',
            headers={'Content-Type': 'application/json'} | kwargs.pop('tokens'),
        ) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(
                    status_code=response.status,
                    detail=await response.text(),
                )
            user_id = (await response.json())['user_id']
            exec_func = kwargs.pop('exec_func')
            kwargs.pop('user_id')
            return await exec_func(*args, user_id=user_id, **kwargs)
