import logging
import signal
import sys
from time import sleep

import click

from commons.asyncio import run_in_loop
from commons.redis import get_redis
from worker.consumers import RandomSleepConsumer
from worker.processors import QueueProcessor
from worker.queues import InMemoryQueue, RedisQueue
from worker.serializers import CreateOrderMessageSerializer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    pass


def setup_signal_handlers(processor: QueueProcessor):
    def handle_signal(signum, frame):
        logger.warning('killing processor signum=%s frame=%s', signum, frame)
        processor.kill()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGQUIT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)


async def consume_memory_tasks(tasks_number: int, concurrency: int) -> None:
    queue = InMemoryQueue()
    serializer = CreateOrderMessageSerializer()
    consumer = RandomSleepConsumer()
    processor = QueueProcessor(queue, serializer, consumer, concurrency=concurrency)

    setup_signal_handlers(processor)

    for i in range(tasks_number):
        queue.enqueue(f'{{"order_number": "{i}"}}')

    await processor.process()


async def consume_redis_tasks(concurrency: int) -> None:
    redis = await get_redis()
    queue = RedisQueue(redis, key='orders')
    serializer = CreateOrderMessageSerializer()
    consumer = RandomSleepConsumer()
    processor = QueueProcessor(queue, serializer, consumer, concurrency=concurrency)

    setup_signal_handlers(processor)

    await processor.process()

    redis.close()
    await redis.wait_closed()


async def push_redis_tasks(tasks_number: int) -> None:
    redis = await get_redis()
    queue = RedisQueue(redis, key='orders')

    for i in range(tasks_number):
        await queue.enqueue(f'{{"order_number": "{i}"}}')

    redis.close()
    await redis.wait_closed()


@cli.command()
@click.option('--concurrency', default=500, help='limit of concurrent in-memory tasks')
@click.option('--tasks', default=1000, help='number of tasks to consume')
def memory_worker(concurrency: int, tasks: int) -> None:
    run_in_loop(consume_memory_tasks(tasks, concurrency))


@cli.command()
@click.option('--number', default=1000, help='number of tasks to consume')
def produce_redis_tasks(number: int) -> None:
    run_in_loop(push_redis_tasks(number))


@cli.command()
@click.option('--concurrency', default=50, help='limit of concurrent in-memory tasks')
def redis_worker(concurrency: int) -> None:
    run_in_loop(consume_redis_tasks(concurrency))


@cli.command()
def keep_sleeping() -> None:
    while True:
        sleep(10)


commands = click.CommandCollection(sources=[cli])


if __name__ == '__main__':
    commands()
