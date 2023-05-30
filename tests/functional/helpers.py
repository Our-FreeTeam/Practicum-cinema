import aiohttp

from settings import test_settings


async def make_get_request(api: str, params: dict, answer_code: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(test_settings.service_url + api, params=params) as response:
            assert response.status == answer_code
            return await response.json()
