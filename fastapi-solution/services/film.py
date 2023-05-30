from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.models import Film
from services.cache_service import AsyncCacheStorage, RedisCacheService
from services.common_service import CommonService

from db.elastic import get_elastic
from db.redis import get_redis


class FilmService(CommonService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        super(FilmService, self).__init__(cache_service=RedisCacheService(cache), elastic=elastic,
                                          model=Film)


@lru_cache()
def get_film_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, elastic)
