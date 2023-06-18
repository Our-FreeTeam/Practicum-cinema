from functools import wraps
from http import HTTPStatus

import aiohttp
import backoff
import messages
import requests
from fastapi import HTTPException
from settings import settings


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
            user = kwargs.get('user_id')
            get_user_id = user if user else kwargs.get('event').user_id
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
