from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.models import Genre
from services.cache_service import AsyncCacheStorage, RedisCacheService
from services.common_service import CommonService

from db.elastic import get_elastic
from db.redis import get_redis


class GenreService(CommonService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        super(GenreService, self).__init__(cache_service=RedisCacheService(cache), elastic=elastic,
                                           model=Genre)


@lru_cache()
def get_genre_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, elastic)
