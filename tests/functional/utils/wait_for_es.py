import backoff
import elasticsearch
from settings import test_settings


@backoff.on_exception(backoff.expo,
                      elasticsearch.exceptions.ConnectionError,
                      max_tries=8,
                      jitter=None)
def connect_check(client):
    if client.search():
        with open("/ES_OK.STATUS", "w") as fp:
            fp.write("ok")


if __name__ == '__main__':
    es_client = elasticsearch.Elasticsearch(hosts=test_settings.elastic_url)
    connect_check(es_client)  # test commit
