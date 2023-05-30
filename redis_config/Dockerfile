FROM redis:alpine3.17

WORKDIR /opt/redis

COPY redis.conf redis.conf


ENTRYPOINT ["redis-server", "/opt/redis/redis.conf"]