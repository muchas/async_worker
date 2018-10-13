import asyncio
from asyncio import Future
from typing import Any, Coroutine
from unittest import mock


def make_future(result: Any) -> Future:
    future = Future()
    future.set_result(result)
    return future


def run_in_loop(coroutine: Coroutine) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)
    loop.close()


class AsyncContextManagerMock(mock.MagicMock):
    async def __aenter__(self):
        return self.aenter

    async def __aexit__(self, *args):
        pass


class AsyncIterator:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item
