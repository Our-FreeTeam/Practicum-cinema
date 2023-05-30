import backoff
import redis
from settings import test_settings


@backoff.on_exception(backoff.expo,
                      redis.exceptions.ConnectionError,
                      max_tries=8,
                      jitter=None)
def connect_check(client):
    if client.set("test_key", "test_ok"):
        with open("/RD_OK.STATUS", "w") as fp:
            fp.write("ok")


if __name__ == '__main__':
    redis_client = redis.Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    connect_check(redis_client)
