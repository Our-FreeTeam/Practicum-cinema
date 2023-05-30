from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from core.config import settings
from models.models import ResponseList
from services.elastic_query_collection import (
    prep_full_query, prep_text_query, prep_genre_query,
    prep_search_after_query)

load_dotenv()


class CommonService:
    def __init__(self, cache_service, elastic: AsyncElasticsearch,
                 model: BaseModel):
        self.elastic = elastic
        self.model = model
        self.index_name = str(self.model.__name__).lower() + 's'
        self.cache_enabled = settings.redis_cache_enabled
        self.cache_service = cache_service

    async def get_by_id(self, entity_id: str) -> BaseModel | None:
        """
        Take UUID of element, and ask Redis Cache,
        and return data if any,
        else
        ask Elastic and return
        """
        entity = None

        if self.cache_enabled:
            entity = await self.cache_service._from_cache(key=entity_id, model=self.model)

        if not entity:
            entity = await self._get_from_elastic(entity_id)
            if not entity:
                return None
            await self.cache_service._put_to_cache(key=entity_id, value=entity)
        return entity

    async def get_list_from_elastic(self, sort: str = 'uuid',
                                    page_size: int = settings.page_size,
                                    last_element: str | None = None, **kwargs) \
            -> ResponseList:
        """ Take filters, convert to hash and search in Redis Cache
            if found, return results from cache,
            otherwise
            ask from elastic
        """
        uuid_list = None

        filter_str = f'{self.index_name}{sort}{page_size}{last_element or None}{kwargs.get("genre") or None}' \
                     f'{kwargs.get("query") or None}'

        if self.cache_enabled:
            uuid_list = await self.cache_service._from_cache(key=filter_str)

        # We cached query for this FILTER in Redis, ask ELASTIC
        if not uuid_list:

            uuid_list = []
            entity_list = await self.get_by_filter(sort, page_size,
                                                   last_element, **kwargs)
            if not entity_list:
                return None

            for element in entity_list.result_list:
                await self.cache_service._put_to_cache(key=str(element.uuid), value=element)
                uuid_list.append(str(element.uuid))

            # Redis Value format
            # LAST_ELEMENT_FROM_FILTER:000_hash_num_of_elem_001,....
            await self.cache_service._put_to_cache(key=filter_str, values_list=",".join(uuid_list),
                                                   last_element=entity_list.last_element)

            return ResponseList(result_list=entity_list.result_list,
                                last_element=entity_list.last_element)

        # We have cache for this Filter, get from REDIS
        else:

            result_list = []
            last_element_from_cache = ""
            data_from_cache = uuid_list.decode('utf-8').split(':')

            if data_from_cache[1]:

                for elem in data_from_cache[1].split(","):
                    elem_from_cache = await self.cache_service._from_cache(key=elem,
                                                                           model=self.model)
                    result_list.append(elem_from_cache)

                if data_from_cache[0]:
                    last_element_from_cache = data_from_cache[0]

                return ResponseList(result_list=result_list,
                                    last_element=last_element_from_cache)
            return None

    async def get_by_filter(self, sort: str = 'uuid', page_size: int = settings.page_size,
                            last_element: str | None = None, **kwargs):

        def prepare_query(query_template: str, query_attribute: str, **kwargs):
            search_fields = '"title", "description", "director",' \
                            ' "actors_names", "writers_names", "full_name"'

            if query_attribute in kwargs.keys():
                query_value = kwargs.get(query_attribute)
                if query_value:
                    if query_attribute == 'query':
                        # перечисляем все поля для полнотекстового поиска
                        return query_template % (search_fields, query_value)
                    return query_template % query_value
            return ''

        sort_order = f'{sort[1:]}:desc' if sort.startswith('-') \
            else f'{sort}:asc'

        try:

            genre_query = prepare_query(prep_genre_query, 'genre', **kwargs)
            text_query = prepare_query(prep_text_query, 'query', **kwargs)

            queries_list = [query for query in [genre_query, text_query] if query]
            last_element_query = prep_search_after_query % last_element if last_element else ''
            full_query = prep_full_query % (','.join(queries_list), last_element_query)

            docs = await self.elastic.search(index=self.index_name,
                                             sort=sort_order,
                                             body=full_query,
                                             size=page_size)

        except NotFoundError:
            return None

        if docs['hits']['hits']:
            last_element = docs['hits']['hits'][-1]['sort'][0]
            result_list = [self.model(**doc['_source']) for doc in
                           docs['hits']['hits']]

            return ResponseList(result_list=result_list,
                                last_element=last_element)
        return ResponseList(result_list=[], last_element=None)

    async def _get_from_elastic(self, entity_id: str) -> BaseModel | None:
        try:
            doc = await self.elastic.get(self.index_name, entity_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])
