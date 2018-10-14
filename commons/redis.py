import aioredis
from aioredis import Redis

from settings import REDIS_HOST, MIN_REDIS_POOL_SIZE, REDIS_PORT, REDIS_DB, MAX_REDIS_POOL_SIZE


async def get_redis() -> Redis:
    return await aioredis.create_redis_pool(f'redis://{REDIS_HOST}:{REDIS_PORT}', db=int(REDIS_DB),
                                            minsize=MIN_REDIS_POOL_SIZE, maxsize=MAX_REDIS_POOL_SIZE)
