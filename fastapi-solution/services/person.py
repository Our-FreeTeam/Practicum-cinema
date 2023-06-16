from functools import lru_cache

from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.models import Person, PersonFilms, PersonFilmsResponse
from services.cache_service import AsyncCacheStorage, RedisCacheService
from services.common_service import CommonService
from services.elastic_query_collection import prep_film_person_query

from db.elastic import get_elastic
from db.redis import get_redis

load_dotenv()


class PersonService(CommonService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        super(PersonService, self).__init__(cache_service=RedisCacheService(cache), elastic=elastic,
                                            model=Person)

    async def get_film_info_for_person(self, film_ids: list[str]) \
            -> PersonFilmsResponse | None:

        str_film_ids = str(film_ids).replace('\'', '"')
        full_query = prep_film_person_query % str_film_ids
        try:
            docs = await self.elastic.search(index='films',
                                             body=full_query)
        except NotFoundError:
            return PersonFilmsResponse()

        if docs['hits']['hits']:
            return PersonFilmsResponse(response_list=[PersonFilms(**doc['_source']) for doc in
                                                      docs['hits']['hits']])
        else:
            return PersonFilmsResponse()


@lru_cache()
def get_person_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, elastic)
