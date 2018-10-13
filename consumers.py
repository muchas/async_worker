import asyncio
import random

from abstract import Consumer, Message


class SleepConsumer(Consumer):

    async def consume(self, message: Message) -> None:
        await asyncio.sleep(0.2 + random.random())  # call to database

        await asyncio.sleep(random.random() * 1.5)  # waiting for lock / critical section
        await asyncio.sleep(1 + random.random() * 3)  # call to external service

        await asyncio.sleep(0.2 + random.random())  # call to database again


class SharedLockConsumer(Consumer):

    async def consume(self, message: Message) -> None:
        # TODO: add lock, randomize
        # TODO: simulate lock
        await asyncio.sleep(3)
