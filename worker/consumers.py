import asyncio
import random

from worker.abstract import Consumer, Message


class ConstantSleepConsumer(Consumer):
    async def consume(self, message: Message) -> None:
        await asyncio.sleep(3)  # call to external service


class RandomSleepConsumer(Consumer):

    async def consume(self, message: Message) -> None:
        await asyncio.sleep(0.2 + random.random())  # call to database

        await asyncio.sleep(random.random() * 1.5)  # waiting for lock / critical section
        await asyncio.sleep(1 + random.random() * 3)  # call to external service

        await asyncio.sleep(0.2 + random.random())  # call to database again


class SharedLockConsumer(Consumer):

    def __init__(self, lock: asyncio.Lock) -> None:
        self._lock = lock

    async def consume(self, message: Message) -> None:
        with self._lock.acquire():
            await asyncio.sleep(3 + random.random())
