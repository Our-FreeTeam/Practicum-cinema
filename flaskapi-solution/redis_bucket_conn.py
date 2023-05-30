import redis
import time

from functools import wraps
from flask import request, jsonify

from settings import settings

redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


def leaky_bucket(request, redis_client, rate, time_period):
    client_ip = request.remote_addr
    key = f"rate_limit:{client_ip}:{request.endpoint}"
    current_time = int(time.time())

    bucket_start_time = redis_client.get(f"{key}:start_time")
    if not bucket_start_time:
        redis_client.set(f"{key}:start_time", current_time)
        redis_client.set(f"{key}:count", 1)
        redis_client.expire(f"{key}:start_time", time_period)
        redis_client.expire(f"{key}:count", time_period)
        return False

    bucket_start_time = int(bucket_start_time)
    count = int(redis_client.get(f"{key}:count"))

    if current_time - bucket_start_time < time_period and count >= rate:
        return True

    if current_time - bucket_start_time >= time_period:
        redis_client.set(f"{key}:start_time", current_time)
        redis_client.set(f"{key}:count", 1)
        redis_client.expire(f"{key}:start_time", time_period)
        redis_client.expire(f"{key}:count", time_period)
    else:
        redis_client.incr(f"{key}:count")

    return False


def rate_limiter(rate, time_period):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            if leaky_bucket(request, redis_client, rate,
                            time_period):  # Pass the request and redis_client here
                response = jsonify({"error": "Too many requests"})
                response.status_code = 429
                return response

            return f(*args, **kwargs)

        return wrapped

    return decorator
