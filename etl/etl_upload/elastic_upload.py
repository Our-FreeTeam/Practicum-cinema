import datetime
import logging

import elastic_transport
import elasticsearch
from elasticsearch import Elasticsearch
from sender.src.utils import log
from sender.src.utils import backoff


class ElasticUpload:
    default_date = datetime.date(1000, 1, 1)

    def __init__(self, client: Elasticsearch, index_name: str):
        self.client = client
        self.index_name = index_name

    @log
    @backoff(exception=elastic_transport.ConnectionError)
    def upload_data(self, data, logger=None):
        errors_here = False
        actions = []

        for row in data:
            action = {"index": {"_index": self.index_name, "_id": row.uuid}}
            actions.append(action)

            del row.modified

            doc = row.json()
            actions.append(doc)

        result = self.client.bulk(index=self.index_name, operations=actions)
        if bool(result['errors']):
            errors_here = True
        return errors_here

    @log
    @backoff(exception=elastic_transport.ConnectionError)
    def get_last_modified(self, logger=None):
        try:
            res = self.client.search(index=f'last_modified_{self.index_name}')
            source = res.body['hits']['hits'][0]['_source']
            last_modified = source['last_modified']
            try_count = source['try_count']
            if last_modified:
                return datetime.datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%S.%f'), try_count
            return self.default_date, 0
        except elasticsearch.NotFoundError:
            logging.warning('Index not found while searching last modified movie')
            return self.default_date, 0
        except IndexError:
            logging.warning('IndexError while searching last modified movie')
            return self.default_date, 0
        except KeyError:
            logging.warning('KeyError while searching last modified movie')
            return self.default_date, 0

    @log
    @backoff(exception=elastic_transport.ConnectionError)
    def set_last_modified(self, last_modified: datetime, try_count: str, logger=None):
        self.client.index(
            index=f'last_modified_{self.index_name}',
            id=1,
            document={'last_modified': datetime.datetime.strftime(last_modified, '%Y-%m-%dT%H:%M:%S.%f'),
                      'try_count': try_count})


class MovieUploader(ElasticUpload):
    def __init__(self, client: Elasticsearch):
        self.client = client
        self.index_name = 'films'


class PersonUploader(ElasticUpload):
    def __init__(self, client: Elasticsearch):
        self.client = client
        self.index_name = 'persons'


class GenreUploader(ElasticUpload):
    def __init__(self, client: Elasticsearch):
        self.client = client
        self.index_name = 'genres'
