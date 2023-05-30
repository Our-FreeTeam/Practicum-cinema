import logging
from contextlib import closing, contextmanager

import psycopg2 as psycopg2
from elasticsearch import Elasticsearch
from etl_upload.elastic_upload import (GenreUploader, MovieUploader,
                                       PersonUploader)
from etl_upload.etl_process import EtlProcess
from etl_upload.postgres_extractor import (GenreExtractor, MovieExtractor,
                                           PersonExtractor)
from psycopg2.extras import DictCursor
from storage_config import es_host, pgdb, settings
from utils import backoff, log


@log
@backoff(exception=psycopg2.OperationalError)
def pg_conn(*args, **kwargs):
    return psycopg2.connect(*args, **kwargs)


@contextmanager
def pg_conn_context(*args, **kwargs):
    connection = pg_conn(*args, **kwargs)
    yield connection
    connection.close()


if __name__ == '__main__':
    logging.basicConfig(format=settings.log_format, level=settings.log_level)

    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect, \
            closing(Elasticsearch(**dict(es_host))) as es_conn:
        match settings.uploaded_index:
            case 'films':
                EtlProcess(settings.uploaded_index, MovieExtractor(pg_connect), MovieUploader(es_conn))
            case 'genres':
                EtlProcess(settings.uploaded_index, PersonExtractor(pg_connect), PersonUploader(es_conn))
            case 'persons':
                EtlProcess(settings.uploaded_index, GenreExtractor(pg_connect), GenreUploader(es_conn))
            case _:
                logging.error('No index was chosen')
