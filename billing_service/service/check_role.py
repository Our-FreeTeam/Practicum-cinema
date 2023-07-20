import json
from functools import wraps

import aiohttp
import backoff
import requests
from fastapi import HTTPException

from core.config import settings


# Проверка роли менеджера, имеющего право смотреть статистику по платежам и подпискам
def check_role(roles: list[str]):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            request = kwargs.get('request')
            tokens = []
            if request:
                tokens = {'access_token': request.headers.get('access_token'),
                          'refresh_token': request.headers.get('refresh_token')}
            return await request_auth(*args, exec_func=func, roles=roles, tokens=tokens, **kwargs)
        return inner
    return func_wrapper


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_tries=8,
                      jitter=None)
async def request_auth(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.AUTH_URL + '/v1/admin/check_role',
                                data=json.dumps({'roles': kwargs.pop('roles')}),
                                headers={'Content-Type': 'application/json'} | kwargs.pop('tokens')) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status,
                                    detail=await response.text())
            exec_func = kwargs.pop('exec_func')
            return await exec_func(*args, **kwargs)
