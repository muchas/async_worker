import asyncio

from abstract import Queue, Job


class InMemoryJob(Job):

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
        return InMemoryJob(task)


class RabbitQueue(Queue):

    async def dequeue(self) -> Job:
        pass


class RedisQueue(Queue):

    async def dequeue(self) -> Job:
        pass

