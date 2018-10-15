import asyncio
import random

from worker.abstract import Consumer, Message


class ConstantSleepConsumer(Consumer):
    async def consume(self, message: Message) -> None:
        await asyncio.sleep(3)  # call to external service


class RandomSleepConsumer(Consumer):

    async def consume(self, message: Message) -> None:
        # query to database / waiting for lock
        # external service call
        await asyncio.sleep(2 + random.random() * 2)
