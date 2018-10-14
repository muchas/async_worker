import logging
import sys

import click

from commons.asyncio import run_in_loop
from worker.consumers import RandomSleepConsumer
from worker.processors import QueueProcessor
from worker.queues import InMemoryQueue
from worker.serializers import CreateOrderMessageSerializer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@click.group()
def cli() -> None:
    pass


async def consume_tasks(tasks_number: int, concurrency: int) -> None:
    queue = InMemoryQueue()
    serializer = CreateOrderMessageSerializer()
    consumer = RandomSleepConsumer()
    processor = QueueProcessor(queue, serializer, consumer, concurrency=concurrency)

    for i in range(tasks_number):
        queue.enqueue(f'{{"order_number": "{i}"}}')

    await processor.process()


@cli.command()
@click.option('--concurrency', default=50, help='limit of concurrent in-memory tasks')
@click.option('--tasks', default=1000, help='number of tasks to consume')
def worker(concurrency: int, tasks: int) -> None:
    run_in_loop(consume_tasks(tasks, concurrency))


commands = click.CommandCollection(sources=[cli])


if __name__ == '__main__':
    commands()
