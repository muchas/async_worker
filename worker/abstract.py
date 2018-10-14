from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    raw_content: str


class Job(metaclass=ABCMeta):

    @property
    @abstractmethod
    def raw_message(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def ack(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def reject(self) -> None:
        raise NotImplementedError()


class MessageSerializer(metaclass=ABCMeta):

    @abstractmethod
    def deserialize(self, raw_message: str) -> Message:
        raise NotImplementedError()


class Consumer(metaclass=ABCMeta):

    @abstractmethod
    async def consume(self, message: Message) -> None:
        raise NotImplementedError()


class Queue(metaclass=ABCMeta):

    @abstractmethod
    async def dequeue(self) -> Job:
        """
        The assumption is that this is a "blocking" call
        - method will suspend until there are jobs in the queue
        """
        raise NotImplementedError()
