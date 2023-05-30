from http import HTTPStatus

from functools import wraps

import aiohttp
import backoff
import requests

from fastapi import HTTPException

import messages
from settings import settings


def is_authorized(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        request = kwargs.get('request')
        if request:
            tokens = {'access_token': request.headers.get('access_token'),
                      'refresh_token': request.headers.get('refresh_token')}
            get_user_id = kwargs.get('user_id') if kwargs.get('user_id') else kwargs.get('event').user_id
        if tokens['access_token']:
            return await request_auth(*args, exec_func=func, tokens=tokens, get_user_id=get_user_id, **kwargs)
        else:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                detail=messages.INCORRECT_TOKEN)
    return inner


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_tries=8,
                      jitter=None)
async def request_auth(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{settings.auth_url}v1/admin/user/{kwargs.pop("get_user_id")}/check_authorization',
                               headers={'Content-Type': 'application/json'} | kwargs.pop('tokens')) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status,
                                    detail=await response.text())
            exec_func = kwargs.pop('exec_func')
            res = await exec_func(*args, **kwargs)
            return res
