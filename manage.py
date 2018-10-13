import asyncio
import logging
import sys

import click

from commons.asyncio import run_in_loop
from consumers import SleepConsumer
from processors import QueueProcessor
from queues import InMemoryQueue
from serializers import CreateOrderMessageSerializer


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@click.group()
def cli() -> None:
    pass


async def produce(queue: InMemoryQueue):
    j = 0
    while True:
        for i in range(100):
            queue.enqueue(f'{{"order_number": "{j}_{i}"}}')

        await asyncio.sleep(1)
        j += 1


async def produce_and_consume(concurrency: int) -> None:
    queue = InMemoryQueue()
    serializer = CreateOrderMessageSerializer()
    consumer = SleepConsumer()
    processor = QueueProcessor(queue, serializer, consumer, concurrency=concurrency)

    await asyncio.gather(*[produce(queue), processor.consume()])


@cli.command()
@click.option('--concurrency', default=500, help='limit of concurrent in-memory tasks')
def worker(concurrency: int) -> None:
    run_in_loop(produce_and_consume(concurrency))


commands = click.CommandCollection(sources=[cli])


if __name__ == '__main__':
    commands()
