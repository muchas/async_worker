import asyncio

from aioredis import Redis

from worker.abstract import Queue, Job


class SimpleJob(Job):

    def __init__(self, raw_message):
        self._raw_message = raw_message

    @property
    def raw_message(self) -> str:
        return self._raw_message

    async def ack(self) -> None:
        pass

    async def reject(self) -> None:
        pass


class InMemoryQueue(Queue):

    def __init__(self):
        self._queue = asyncio.Queue()

    def enqueue(self, raw_task: str) -> None:
        self._queue.put_nowait(raw_task)

    async def dequeue(self) -> Job:
        task = await self._queue.get()
        return SimpleJob(task)


class RedisQueue(Queue):

    def __init__(self, redis: Redis, key: str):
        self._redis = redis
        self._key = key

    async def enqueue(self, raw_task: str) -> None:
        await self._redis.rpush(self._key, raw_task)

    async def dequeue(self) -> Job:
        task = await self._redis.blpop(self._key)
        return SimpleJob(task)
