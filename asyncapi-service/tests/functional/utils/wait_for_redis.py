import os

from redis import Redis
from dotenv import load_dotenv

from tools import backoff

load_dotenv()

redis_host: str = os.environ.get('REDIS_HOST', default='127.0.0.1')
redis_port: int = int(os.environ.get('REDIS_PORT', default=63790))


def ping_redis(redis: Redis) -> bool:
    return redis.ping()


@backoff()
def wait_for_redis():
    redis = Redis(host=redis_host, port=redis_port)
    ping_redis(redis)

    redis.close()


if __name__ == '__main__':
    wait_for_redis()
