import asyncio
import logging
from asyncio import Task
from typing import Dict

from worker.abstract import MessageSerializer, Queue, Consumer, Job

logger = logging.getLogger(__name__)


class QueueProcessor:
    """
    Responsibility: passing jobs from the given queue
    to the consumer in asynchronous manner

    This class is a proof of concept.
    """

    def __init__(self,
                 queue: Queue,
                 serializer: MessageSerializer,
                 consumer: Consumer,
                 concurrency: int = 500) -> None:
        self._consumer = consumer
        self._serializer = serializer
        self._queue = queue
        self._jobs_limit = concurrency
        self._tasks: Dict[int, Task] = {}
        self._is_running = True

    async def process(self) -> None:
        while self._is_running:
            await self._schedule_pending_jobs()
            await asyncio.wait(self._tasks.values(), return_when=asyncio.FIRST_COMPLETED)

        await asyncio.gather(*self._tasks.values())  # wait for tasks that have not finished yet

    def kill(self):
        self._is_running = False

    async def _schedule_pending_jobs(self) -> None:
        while len(self._tasks) < self._jobs_limit:
            job = await self._queue.dequeue()

            task = asyncio.create_task(self._process_job(job))

            self._tasks[id(task)] = task
            task.add_done_callback(self._handle_done_task)

    async def _process_job(self, job: Job) -> None:
        try:
            logger.debug('processing job message=%s processing_jobs=%s', job.raw_message, len(self._tasks))

            message = self._serializer.deserialize(job.raw_message)
            await self._consumer.consume(message)
            await job.ack()
        except Exception:
            await job.reject()
            logger.exception('message could not be consumed message=%s', job.raw_message)
        finally:
            logger.debug('finished job message=%s processing_jobs=%s', job.raw_message, len(self._tasks))

    def _handle_done_task(self, future: asyncio.Future) -> None:
        del self._tasks[id(future)]
