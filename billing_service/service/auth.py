import aiohttp

from core.config import settings


async def get_token(session):
    auth_url = settings.auth_url
    async with session.post(
            f'{auth_url}v1/auth/login', json={"user": settings.auth_user, "password": settings.auth_password}) as token:
        headers = {}
        if (token.headers.get("access_token") is not None and
                token.headers.get("refresh_token") is not None):
            headers['access_token'] = token.headers.get("access_token")
            headers['refresh_token'] = token.headers.get("refresh_token")
        return headers


async def assign_role():
    async with aiohttp.ClientSession() as session:
        token_headers = await get_token(session)

