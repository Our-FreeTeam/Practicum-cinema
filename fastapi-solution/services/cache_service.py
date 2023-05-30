import hashlib
from abc import abstractmethod, ABC

from pydantic import BaseModel
from redis.asyncio.client import Redis

from core.config import settings


def get_hash(elem_id: str = "") -> str:
    return hashlib.md5(str(elem_id).encode()).hexdigest()


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def _from_cache(self, **kwargs):
        pass

    @abstractmethod
    async def _put_to_cache(self, **kwargs):
        pass


class RedisCacheService(AsyncCacheStorage):
    """Use Redis server as cache server for project
       There are two classes:
        _from_cache(key:str, model:BaseModel) - get data by key
                                                from cache or None
        _to_cache(key:str, value:str, values_list:str, last_index:str,
         model:BaseModel) - put data to cache
    """

    def __init__(self, redis: Redis):
        self.cache = redis
        self.CACHE_EXPIRE_ITEM = settings.cache_expire + 60
        self.CACHE_EXPIRE_LIST = settings.cache_expire

    async def _from_cache(self, **kwargs) -> BaseModel | str | None:
        """Get LIST data from cache by key arg,
           or get Item data by key and model (Film, Genre, Person..)
        """
        data = await self.cache.get(get_hash(kwargs.get('key')))
        if not data:
            return

        if kwargs.get('model'):
            return_data = kwargs.get('model').parse_raw(data)
            return return_data

        return data

    async def _put_to_cache(self, **kwargs):
        """
        Put data to cache, params:
          id - uuid of of item (str)
          value - value to put to cache (str)
          or values_list - put list of items as value (str)
          last_element - element to start from next time (param)
        """
        if kwargs.get('key'):

            if kwargs.get('values_list'):
                data_for_cache = f'{kwargs.get("last_element")}:{kwargs.get("values_list")}'
                await self.cache.set(get_hash(kwargs.get('key')),
                                     data_for_cache,
                                     self.CACHE_EXPIRE_LIST)

            else:
                if kwargs.get('value'):
                    hash_key = get_hash(str(kwargs.get('value').uuid))
                    await self.cache.set(hash_key, kwargs.get('value').json(),
                                         self.CACHE_EXPIRE_ITEM)
